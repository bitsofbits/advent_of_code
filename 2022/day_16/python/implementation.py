import re
from math import inf
from typing import NamedTuple, Tuple

example_text = """
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
"""


class Node(NamedTuple):
    label: str
    flow: int
    dests: Tuple[(str, int)]


def parse_graph(text):
    """Load text graph into linked dicts

    >>> nodes = parse_graph(example_text)
    >>> keys = list(nodes)
    >>> for nd in [nodes[k] for k in keys]: print(nd)
    Node(label='AA', flow=0, dests=(('DD', 1), ('II', 1), ('BB', 1)))
    Node(label='BB', flow=13, dests=(('CC', 1), ('AA', 1)))
    Node(label='CC', flow=2, dests=(('DD', 1), ('BB', 1)))
    Node(label='DD', flow=20, dests=(('CC', 1), ('AA', 1), ('EE', 1)))
    Node(label='EE', flow=3, dests=(('FF', 1), ('DD', 1)))
    Node(label='FF', flow=0, dests=(('EE', 1), ('GG', 1)))
    Node(label='GG', flow=0, dests=(('FF', 1), ('HH', 1)))
    Node(label='HH', flow=22, dests=(('GG', 1),))
    Node(label='II', flow=0, dests=(('AA', 1), ('JJ', 1)))
    Node(label='JJ', flow=21, dests=(('II', 1),))
    """
    nodes = {}
    p = re.compile(
        r"Valve ([A-Z][A-Z]) has flow rate=(\d*); "
        "tunnels? leads? to valves? ((?:[A-Z][A-Z], )*(?:[A-Z][A-Z]))"
    )
    for line in text.strip().split("\n"):
        line = line.strip()
        if line:
            g = p.match(line).groups()
            lbl = g[0]
            flow = int(g[1])
            dests = tuple((x.strip(), 1) for x in g[2].split(","))
            nodes[lbl] = Node(lbl, flow, dests)
    return nodes


def simplify(nodes, preserve={"AA"}, preserve_nonzero=True):
    """
    >>> nodes = simplify(parse_graph(example_text), preserve={"AA"})
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=(('BB', 1), ('DD', 1), ('JJ', 2)))
    Node(label='BB', flow=13, dests=(('AA', 1), ('CC', 1)))
    Node(label='CC', flow=2, dests=(('BB', 1), ('DD', 1)))
    Node(label='DD', flow=20, dests=(('AA', 1), ('CC', 1), ('EE', 1)))
    Node(label='EE', flow=3, dests=(('DD', 1), ('HH', 3)))
    Node(label='HH', flow=22, dests=(('EE', 3),))
    Node(label='JJ', flow=21, dests=(('AA', 2),))
    """
    if preserve_nonzero:
        preserve = set(preserve)
        for k, v in nodes.items():
            if v.flow > 0:
                preserve.add(k)
    nodes = nodes.copy()
    for k in list(nodes):
        nd = nodes[k]
        nodes[k] = Node(nd.label, nd.flow, set(nd.dests))
    while True:
        parents = {k: set() for k in nodes}
        for k, nd in nodes.items():
            for d, c in nd.dests:
                parents[d].add((k, c))
        for k in list(nodes):
            nd_k = nodes[k]
            if k not in preserve:
                for p, c0 in parents[k]:
                    nd_p = nodes[p]
                    new_dests = {d: c for (d, c) in nd_p.dests if d != k}
                    for d, c in nd_k.dests:
                        if d != p:
                            new_dests[d] = min(c + c0, new_dests.get(d, inf))
                    nodes[p] = Node(nd_p.label, nd_p.flow, set(new_dests.items()))
                del nodes[k]
                break
        else:
            break
    for k in list(nodes):
        nd = nodes[k]
        assert nd.label == k
        dests = tuple(sorted(nd.dests))
        nodes[k] = Node(nd.label, nd.flow, dests)
    return nodes


def _merge_edges(d1, d2, k):
    dmap = dict(d1)
    for d, c in d2:
        if c < dmap.get(d, inf):
            dmap[d] = c
    assert set(dict(d2).keys()) == {k}, list(dmap.keys())
    return sorted(dmap.items())


def add_paths(nodes):
    """Add shortest path between every node

    >>> nodes = simplify(parse_graph(example_text), preserve={"AA"})
    >>> add_paths(nodes)
    >>> for k in sorted(nodes): print(nodes[k])  # doctest: +ELLIPSIS
    Node(label='AA', flow=0, dests=(('BB', 1), ('CC', 2), ('DD', 1), ('EE', 2), ...
    Node(label='BB', flow=13, dests=(('AA', 1), ('CC', 1), ('DD', 2), ('EE', 3),...
    Node(label='CC', flow=2, dests=(('AA', 2), ('BB', 1), ('DD', 1), ('EE', 2), ...
    Node(label='DD', flow=20, dests=(('AA', 1), ('BB', 2), ('CC', 1), ('EE', 1),...
    Node(label='EE', flow=3, dests=(('AA', 2), ('BB', 3), ('CC', 2), ('DD', 1), ...
    Node(label='HH', flow=22, dests=(('AA', 5), ('BB', 6), ('CC', 5), ('DD', 4),...
    Node(label='JJ', flow=21, dests=(('AA', 2), ('BB', 3), ('CC', 4), ('DD', 3),...
    """
    # Use the [Floyd–Warshall algorithm]
    # (https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)
    # Normally would use numpy, but I'm using vanilla python for everything
    labels = list(nodes)
    n = len(labels)
    cost = {(i, j): inf for i in range(n) for j in range(n)}
    pmap = {k: i for (i, k) in enumerate(labels)}
    for k, nd in nodes.items():
        i = pmap[k]
        for d, c in nd.dests:
            j = pmap[d]
            cost[i, j] = c
        cost[i, i] = 0
    for k in range(n):
        for i in range(n):
            for j in range(n):
                cost[i, j] = min(cost[i, j], cost[i, k] + cost[k, j])

    for k in labels:
        i = pmap[k]
        dests = tuple((d, cost[i, pmap[d]]) for d in labels if d != k)
        nodes[k] = Node(label=k, flow=nodes[k].flow, dests=dests)


def setup_nodes(graph):
    """Convert nodes to faster form for traversal"""
    nodes = {}
    kmap = {k: 1 << i for (i, k) in enumerate(sorted(set(graph)))}
    # Use a simpler data structure: k : (flow, ((d, cost), ...)
    # Here k and d are bit field keys.
    for k, nd in graph.items():
        nodes[kmap[k]] = (
            nd.flow,
            # We always turn on a valve, so bump the cost here to save op later.
            tuple((kmap[d], c + 1) for (d, c) in nd.dests),
        )
    return kmap["AA"], nodes


def condense_state_map(state_map, start):
    # We remove AA from the keys because that break the comparisons in part 2.
    score_map = {}
    for (k, t), v in state_map.items():
        k &= ~start
        score_map[k] = max(v, score_map.get(k, 0))
    return score_map


def traverse(graph, time_left, return_map=False):
    """traverse caves within time_limit trying to maximize released steam

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> traverse(nodes, 30)
    1651
    """
    start, nodes = setup_nodes(graph)
    state_map = {}
    pending = [(start, time_left, 0, start)]
    while pending:
        k, t, score, opened = pending.pop()
        flow, dests = nodes[k]
        score += flow * t * (k & opened == 0)
        opened |= k
        state = (opened, time_left)
        if state_map.get(state, 0) > score:
            continue
        state_map[state] = score
        for d, c in dests:
            if d & opened == 0 and t - c > 0:
                pending.append((d, t - c, score, opened))
    if return_map:
        return condense_state_map(state_map, start)
    else:
        return max(state_map.values())


def dual_traverse(graph, time_left):
    """Find the best score for two agents traversing the caves at once

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> dual_traverse(nodes, 26)
    1707
    """
    score_map = traverse(graph, time_left, return_map=True)
    pairs = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
    best = 0
    for i, (k1, v1) in enumerate(pairs):
        for k2, v2 in pairs[i + 1 :]:
            total = v1 + v2
            if total <= best:
                # Since pairs are sorted by reverse score, the rest of k2 won't help
                break
            if not k1 & k2:
                best = max(best, total)
    return best


if __name__ == "__main__":
    import doctest

    doctest.testmod()
