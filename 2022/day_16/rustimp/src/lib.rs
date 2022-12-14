use once_cell::sync::Lazy;
use regex::Regex;
use std::collections::HashMap;

use std::collections::HashSet;

#[allow(dead_code)]
const EXAMPLE_TEXT: &str = r#"
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"#;

#[derive(Clone)]
pub struct Node<T> {
    flow: isize,
    dests: Vec<(T, isize)>,
}

const NODE_RE: Lazy<Regex> = Lazy::new(|| {
    Regex::new(r"^Valve ([A-Z][A-Z]) has flow rate=(\d*); tunnels? leads? to valves? ((?:[A-Z][A-Z], )*(?:[A-Z][A-Z]))$").unwrap()
});

impl Node<String> {
    fn parse_node(line: &str) -> (String, Node<String>) {
        let caps = NODE_RE.captures(line).unwrap();
        let lbl = caps.get(1).unwrap().as_str();
        let flow = caps.get(2).unwrap().as_str().parse::<isize>().unwrap();
        let dests_text = caps.get(3).unwrap().as_str();
        let mut dests = Vec::new();
        for d in dests_text.split(",") {
            dests.push((d.trim().to_string(), 1));
        }
        (lbl.to_string(), Node { flow, dests })
    }

    pub fn parse_graph(text: &str) -> HashMap<String, Node<String>> {
        HashMap::from_iter(text.trim().split("\n").map(|x| Node::parse_node(x)))
    }
}

impl Node<usize> {
    pub fn from_string_based_graph(
        nodes: HashMap<String, Node<String>>,
        root: &str,
    ) -> (HashMap<usize, Node<usize>>, usize) {
        let key_set: HashSet<String> = HashSet::from_iter(nodes.iter().map(|(k, _)| k.clone()));
        let mut keys = key_set.iter().collect::<Vec<&String>>();
        keys.sort();
        let key_map: HashMap<String, usize> =
            HashMap::from_iter(keys.iter().enumerate().map(|(k, v)| (v.to_string(), k)));
        let mut isize_nodes = HashMap::new();
        for (k, nd) in nodes {
            let dests = nd.dests.iter().map(|(d, c)| (key_map[d], *c)).collect();
            isize_nodes.insert(
                key_map[&k],
                Node {
                    flow: nd.flow,
                    dests,
                },
            );
        }
        (isize_nodes, key_map[root])
    }
}

pub fn add_all_paths(mut nodes: HashMap<usize, Node<usize>>) -> HashMap<usize, Node<usize>> {
    let keys: Vec<usize> = nodes.clone().keys().map(|k| *k).collect();
    let large_value = (keys.iter().max().unwrap_or(&0) + 1) as isize;
    // let n = keys.len();
    let mut cost: HashMap<(usize, usize), isize> = HashMap::new();
    for i in &keys {
        for j in &keys {
            cost.insert((*i, *j), large_value);
        }
    }
    for k in &keys {
        let nd = nodes[k].clone();
        for (d, c) in &nd.dests {
            cost.insert((*k, *d), *c);
        }
        cost.insert((*k, *k), 0);
    }
    for k in &keys {
        for i in &keys {
            for j in &keys {
                let existing = cost[&(*i, *j)];
                let candidate = cost[&(*i, *k)] + cost[&(*k, *j)];
                if candidate < existing {
                    cost.insert((*i, *j), candidate);
                }
            }
        }
    }
    for k in &keys {
        let dests: Vec<(usize, isize)> = Vec::from_iter(
            keys.clone()
                .iter()
                .filter(|d| d != &k)
                .map(|d| (*d, cost[&(*k, *d)])),
        );
        let flow = nodes[k].flow;
        nodes.insert(*k, Node { flow, dests });
    }
    nodes
}

pub fn drop_nodes_with_zero_flow(
    mut nodes: HashMap<usize, Node<usize>>,
    root: usize,
) -> HashMap<usize, Node<usize>> {
    let preserve: HashSet<usize> = HashSet::from_iter(
        nodes
            .iter()
            .filter(|(k, v)| v.flow != 0 || **k == root)
            .map(|(k, _)| *k),
    );
    let keys: Vec<usize> = nodes.clone().keys().map(|k| *k).collect();
    for k in &keys {
        if !preserve.contains(k) {
            nodes.remove(k);
        } else {
            let nd = &nodes[k];
            let flow = nd.flow;
            let dests = Vec::from_iter(
                nd.dests
                    .iter()
                    .filter(|(d, _)| (d != k) && preserve.contains(d))
                    .map(|(k, v)| (*k, *v)),
            );
            nodes.insert(*k, Node { flow, dests });
        }
    }
    nodes
}

fn setup_fast_graph(
    nodes: &HashMap<usize, Node<usize>>,
    root: &usize,
) -> (Vec<Node<usize>>, usize) {
    let mut keys = Vec::from_iter(nodes.iter().map(|(k, _)| k));
    keys.sort();
    let kmap: HashMap<&usize, usize> =
        HashMap::from_iter(keys.iter().enumerate().map(|(k, v)| (*v, k)));
    let mut new = Vec::new();
    for k in &keys {
        let nd = &nodes[k];
        let flow = nd.flow;
        // We always turn on valves that we visit, so just incorporate that into the cost now
        let dests = Vec::from_iter(
            nd.dests
                .iter()
                .filter(|(d, _)| d != root)
                .map(|(d, c)| (kmap[&*d], c + 1)),
        );
        let new_nd = Node { flow, dests };
        new.push(new_nd);
    }
    (new, kmap[root])
}

fn general_traverse(
    graph: &HashMap<usize, Node<usize>>,
    root: &usize,
    time_left: &isize,
) -> (HashMap<(usize, isize), isize>, usize) {
    let (nodes, root) = setup_fast_graph(graph, root);
    let mut state_map = HashMap::new();
    let mut pending = vec![(root, *time_left, 0, 0)];
    while let Some((k, t, score, opened)) = pending.pop() {
        let nd = &nodes[k];
        let score = score + nd.flow * t;
        let opened = opened | 1 << k;
        let state = (opened, t);
        if state_map.get(&state).unwrap_or(&0) > &score {
            continue;
        }
        state_map.insert(state, score);
        for (d, c) in &nd.dests {
            let next_t = &t - c;
            if (next_t > 0) && ((opened & (1 << d)) == 0) {
                pending.push((*d, next_t, score, opened));
            }
        }
    }
    (state_map, root)
}

pub fn traverse(graph: &HashMap<usize, Node<usize>>, root: &usize) -> isize {
    let (state_map, _) = general_traverse(graph, root, &30);
    state_map.iter().map(|(_, v)| *v).max().unwrap_or(0)
}

pub fn dual_traverse(graph: &HashMap<usize, Node<usize>>, root: &usize) -> isize {
    let (state_map, root) = general_traverse(graph, root, &26);
    let mut score_map: HashMap<usize, isize> = HashMap::new();
    for ((k, _t), mut v) in state_map {
        let k = k & !(1 << root);
        if score_map.contains_key(&k) {
            v = v.max(score_map[&k]);
        }
        score_map.insert(k, v);
    }
    let mut pairs: Vec<(usize, isize)> = score_map.iter().map(|(k, v)| (*k, *v)).collect();
    pairs.sort_by(|(_, v1), (_, v2)| v2.cmp(&v1));
    let mut best = 0;
    for (i, (k1, v1)) in pairs.iter().enumerate() {
        for (k2, v2) in pairs[i + 1..].iter() {
            let total = v1 + v2;
            if total <= best {
                break;
            }
            if (k1 & k2) == 0 {
                best = best.max(total);
            }
        }
    }
    best
}

#[test]
fn test_dual_traverse() {
    let nodes = Node::parse_graph(EXAMPLE_TEXT);
    let (mut nodes, root) = Node::from_string_based_graph(nodes, "AA");
    nodes = add_all_paths(nodes);
    nodes = drop_nodes_with_zero_flow(nodes, root);
    let n = dual_traverse(&nodes, &root);
    assert_eq!(n, 1707);
}

#[test]
fn test_traverse() {
    let nodes = Node::parse_graph(EXAMPLE_TEXT);
    let (mut nodes, root) = Node::from_string_based_graph(nodes, "AA");
    nodes = add_all_paths(nodes);
    nodes = drop_nodes_with_zero_flow(nodes, root);
    let n = traverse(&nodes, &root);
    assert_eq!(n, 1651);
}

#[test]
fn test_parse_node() {
    let (k, nd) = Node::parse_node("Valve BB has flow rate=13; tunnels lead to valves CC, AA");
    assert_eq!(k, "BB");
    assert_eq!(nd.flow, 13);
    assert_eq!(nd.dests.len(), 2);
    // assert_eq!(nd.dests["AA"], 1);
}

#[test]
fn test_parse_graph() {
    let nodes = Node::parse_graph(EXAMPLE_TEXT);
    assert_eq!(nodes.len(), 10);
    let aa = &nodes["AA"];
    assert_eq!(aa.flow, 0);
    for (_k, nd) in &nodes {
        let mut dests = nd.dests.clone();
        dests.sort();
        dests.dedup_by_key(|(d, _c)| d.to_string());
        assert!(nd.dests.len() == dests.len());
    }
}

#[test]
fn test_add_all_paths() {
    let nodes = Node::parse_graph(EXAMPLE_TEXT);
    let (mut nodes, root) = Node::from_string_based_graph(nodes, "AA");
    nodes = add_all_paths(nodes);
    nodes = drop_nodes_with_zero_flow(nodes, root);
    assert_eq!(nodes.len(), 7);
    for (_k, nd) in &nodes {
        let mut dests = nd.dests.clone();
        dests.sort();
        dests.dedup_by_key(|(d, _c)| d.to_string());
        assert!(nd.dests.len() == dests.len());
    }
}
