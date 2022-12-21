import re
from concurrent.futures import ProcessPoolExecutor, as_completed
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


def _traverse_from(lbl, nodes, time_left, score_map, score, opened, ALL):
    if time_left < 2:
        return score

    time_left -= 1

    flow, dests = nodes[lbl]
    lcl_score = score + flow * time_left * (lbl & opened == 0)

    opened |= lbl
    score_map[opened] = max(lcl_score, score_map.get(opened, 0))

    if opened == ALL:
        return lcl_score

    result = lcl_score
    for (d, c) in dests:
        if (d & opened == 0) and time_left - c > 1:
            result = max(
                result,
                _traverse_from(
                    d, nodes, time_left - c, score_map, lcl_score, opened, ALL
                ),
            )

    return result


def traverse_from(nd, nodes, time_left):
    """Stub so that we can return score_map while using multiprocessing"""
    score_map = {}
    ALL = 2 ** len(nodes) - 1
    released = _traverse_from(
        nd, nodes, time_left, score_map, score=0, opened=0, ALL=ALL
    )
    return released, score_map


def setup_nodes(graph):
    """Convert nodes to faster form for traversal"""
    nodes = {}
    # Convert keys to bit fields so comparisons are faster
    keys = set()
    for k in graph:
        if k != "AA":
            keys |= {k}
    kmap = {k: 1 << i for (i, k) in enumerate(sorted(keys))}
    # We don't need AA in the final graph, just as starting points, so remove now.
    starts = [(kmap[d], c) for (d, c) in graph["AA"].dests]
    # Use a simpler data structure
    for k, nd in graph.items():
        if k != "AA":
            nodes[kmap[k]] = (
                nd.flow,
                tuple((kmap[d], c) for (d, c) in nd.dests if d != "AA"),
            )
    assert all(f > 0 for (f, _) in nodes.values())
    return starts, nodes


def traverse(graph, time_left, return_map=False):
    """traverse caves within time_limit trying to maximize released steam

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> traverse(nodes, 30)
    1651
    """
    starts, nodes = setup_nodes(graph)
    score = 0
    score_map = {}
    # This problem can be solved in parallel if we treat all the places
    #  we can start from (all places reachable from AA) as separate problems
    with ProcessPoolExecutor() as exe:
        futures = []
        for nd, cost in starts:
            f = exe.submit(traverse_from, nd, nodes, time_left - cost)
            futures.append(f)
        for f in as_completed(futures):
            r, m = f.result()
            score = max(score, r)
            for k, v in m.items():
                score_map[k] = max(v, score_map.get(k, 0))
    if return_map:
        # This is used to solve part 2.
        return score_map
    else:
        return score


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
