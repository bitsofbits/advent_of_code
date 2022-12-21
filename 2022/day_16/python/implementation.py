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


def extract(text):
    if text[-1] in ",:":
        text = text[:-1]
    text = text.split("=")[1]
    return int(text)


def condense(dests):
    dmap = {k: inf for (k, _) in dests}
    for k, cst in dests:
        dmap[k] = min(cst, dmap[k])
    return tuple(dmap.items())


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


def _merge(d1, d2, k):
    dmap = dict(d1)
    for d, c in d2:
        if c < dmap.get(d, inf):
            dmap[d] = c
    assert set(dict(d2).keys()) == {k}, list(dmap.keys())
    return sorted(dmap.items())


def add_paths(nodes):
    """
    >>> nodes = simplify(parse_graph(example_text), preserve={"AA"})
    >>> add_paths(nodes)
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=[('BB', 1), ('CC', 2), ('DD', 1), ('EE', 2), ('HH', 5), ('JJ', 2)])
    Node(label='BB', flow=13, dests=[('AA', 1), ('CC', 1), ('DD', 2), ('EE', 3), ('HH', 6), ('JJ', 3)])
    Node(label='CC', flow=2, dests=[('AA', 2), ('BB', 1), ('DD', 1), ('EE', 2), ('HH', 5), ('JJ', 4)])
    Node(label='DD', flow=20, dests=[('AA', 1), ('BB', 2), ('CC', 1), ('EE', 1), ('HH', 4), ('JJ', 3)])
    Node(label='EE', flow=3, dests=[('AA', 2), ('BB', 3), ('CC', 2), ('DD', 1), ('HH', 3), ('JJ', 4)])
    Node(label='HH', flow=22, dests=[('AA', 5), ('BB', 6), ('CC', 5), ('DD', 4), ('EE', 3), ('JJ', 7)])
    Node(label='JJ', flow=21, dests=[('AA', 2), ('BB', 3), ('CC', 4), ('DD', 3), ('EE', 4), ('HH', 7)])
    """
    labels = list(nodes)
    for a in labels:
        for b in labels:
            if a <= b:
                continue
            simple = simplify(nodes, preserve={a, b}, preserve_nonzero=False)
            A = nodes[a]
            A_dests = _merge(A.dests, simple[a].dests, b)
            nodes[a] = Node(label=a, flow=A.flow, dests=A_dests)
            B = nodes[b]
            B_dests = _merge(B.dests, simple[b].dests, a)
            nodes[b] = Node(label=b, flow=B.flow, dests=B_dests)


def setup_nodes(graph):
    nodes = {}
    # We don't need AA in the final graph, just as starting points, so remove now.
    starts = graph["AA"].dests
    for k, nd in graph.items():
        if k == "AA":
            continue
        nodes[k] = (nd.flow, tuple((d, c) for (d, c) in nd.dests if d != "AA"))
    opened = frozenset(k for (k, v) in graph.items() if v.flow == 0 and k != "AA")
    return starts, nodes, opened


def core(lbl, nodes, time_left, opened, score, score_map):
    if time_left < 2 or len(opened) == len(nodes):
        score_map[opened] = max(score, score_map.get(opened, 0))
        return score

    flow, dests = nodes[lbl]
    lcl_score = score + flow * (time_left - 1) * (lbl not in opened)

    opened = frozenset(opened | {lbl})
    score_map[opened] = max(lcl_score, score_map.get(opened, 0))

    result = lcl_score
    for (d, c) in dests:
        if d not in opened and time_left - c > 2:
            result = max(
                result,
                core(d, nodes, time_left - c - 1, opened, lcl_score, score_map),
            )

    return result


def traverse_mp(nd, nodes, time_left, opened):
    score_map = {}
    released = core(nd, nodes, time_left, opened, 0, score_map)
    return released, score_map


def traverse(graph, time_left, return_map=False):
    """traverse graph within time_limit

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> traverse(nodes, 30)
    1651

    2286
    """
    starts, nodes, opened = setup_nodes(graph)
    score = 0
    score_map = {}
    with ProcessPoolExecutor() as exe:
        futures = []
        for nd, cost in starts:
            f = exe.submit(traverse_mp, nd, nodes, time_left - cost, opened)
            futures.append(f)
        for f in as_completed(futures):
            r, m = f.result()
            score = max(score, r)
            for k, v in m.items():
                score_map[k] = max(v, score_map.get(k, 0))
    if return_map:
        return score_map
    else:
        return score


def int_key(kset, kmap):
    key = 0
    for k in kset:
        key |= kmap[k]
    return key


def dual_traverse(graph, time_left):
    """
    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> dual_traverse(nodes, 26)
    1707
    """
    score_map = traverse(graph, time_left, return_map=True)
    # Convert keys to bitfields so comparisons are faster
    keys = set()
    for k in score_map:
        keys |= k
    kmap = {k: 1 << i for (i, k) in enumerate(keys)}
    score_map = {int_key(k, kmap): v for (k, v) in score_map.items()}
    # Try all compatible combinations, meaning they didn't both turn
    # on a valve
    best = 0
    keys = list(score_map)
    for i, k1 in enumerate(keys):
        for k2 in keys[i + 1 :]:
            if not k1 & k2:
                best = max(best, score_map[k1] + score_map[k2])

    return best


if __name__ == "__main__":
    import doctest

    doctest.testmod()
