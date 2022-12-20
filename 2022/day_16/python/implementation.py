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


def simplify_AA(nodes):
    """Simplify away the AA node, then add back in the connections from AA

    >>> nodes = simplify_AA(parse_graph(example_text))
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=(('BB', 1), ('DD', 1), ('JJ', 2)))
    Node(label='BB', flow=13, dests=(('CC', 1), ('DD', 2), ('JJ', 3)))
    Node(label='CC', flow=2, dests=(('BB', 1), ('DD', 1)))
    Node(label='DD', flow=20, dests=(('BB', 2), ('CC', 1), ('EE', 1), ('JJ', 3)))
    Node(label='EE', flow=3, dests=(('DD', 1), ('HH', 3)))
    Node(label='HH', flow=22, dests=(('EE', 3),))
    Node(label='JJ', flow=21, dests=(('BB', 3), ('DD', 3)))
    """
    s1 = simplify(nodes, preserve={"AA"})
    s2 = simplify(nodes, preserve=())
    s2["AA"] = s1["AA"]
    return s2


def add_paths(nodes):
    """
    >>> nodes = simplify(parse_graph(example_text), preserve={"AA"})
    >>> add_paths(nodes)
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=(('BB', 1), ('CC', 2), ('DD', 1), ('EE', 2), ('HH', 5), ('JJ', 2)))
    Node(label='BB', flow=13, dests=(('AA', 1), ('CC', 1), ('DD', 2), ('EE', 3), ('HH', 6), ('JJ', 3)))
    Node(label='CC', flow=2, dests=(('AA', 2), ('BB', 1), ('DD', 1), ('EE', 2), ('HH', 5), ('JJ', 4)))
    Node(label='DD', flow=20, dests=(('AA', 1), ('BB', 2), ('CC', 1), ('EE', 1), ('HH', 4), ('JJ', 3)))
    Node(label='EE', flow=3, dests=(('AA', 2), ('BB', 3), ('CC', 2), ('DD', 1), ('HH', 3), ('JJ', 4)))
    Node(label='HH', flow=22, dests=(('AA', 5), ('BB', 6), ('CC', 5), ('DD', 4), ('EE', 3), ('JJ', 7)))
    Node(label='JJ', flow=21, dests=(('AA', 2), ('BB', 3), ('CC', 4), ('DD', 3), ('EE', 4), ('HH', 7)))
    """
    labels = list(nodes)
    for a in labels:
        for b in labels:
            if a <= b:
                continue
            simple = simplify(nodes, preserve={a, b}, preserve_nonzero=False)
            A = nodes[a]
            dests = tuple(sorted(set(A.dests) | set(simple[a].dests)))
            nodes[a] = Node(label=a, flow=A.flow, dests=dests)
            B = nodes[b]
            dests = tuple(sorted(set(B.dests) | set(simple[b].dests)))
            nodes[b] = Node(label=b, flow=B.flow, dests=dests)


def setup_nodes(graph):
    nodes = {}
    for k, nd in graph.items():
        nodes[k] = (nd.flow, tuple((d, c) for (d, c) in nd.dests))
    opened = frozenset(k for (k, v) in graph.items() if v.flow == 0)
    return nodes, opened


def _traverse(lbl, nodes, time_left, opened, states):
    if time_left <= 1 or len(opened) == len(nodes):
        return 0

    key = (time_left, lbl, opened)

    if key in states:
        return states[key]

    flow, dests = nodes[lbl]

    lcl_score = flow * (time_left - 1) * (lbl not in opened)
    released = lcl_score

    opened = frozenset(opened | {lbl})
    for (d, c) in dests:
        if d not in opened and time_left - c > 2:
            released = max(
                released,
                _traverse(d, nodes, time_left - c - 1, opened, states) + lcl_score,
            )

    states[key] = released
    return released


def traverse(graph, time_left):
    """traverse graph within time_limit

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> traverse(nodes, 30)
    1651
    """
    nodes, opened = setup_nodes(graph)
    released = 0
    _, dests = nodes["AA"]
    with ProcessPoolExecutor() as exe:
        futures = []
        for nd, cost in dests:
            f = exe.submit(_traverse, nd, nodes, time_left - cost, opened, states={})
            futures.append(f)
        for f in as_completed(futures):
            released = max(released, f.result())
    return released


def _dispatch(lbl, other_lbl_tl, nodes, time_left, opened, states):
    assert time_left >= 0
    flow, dests = nodes[lbl]
    olbl, otl = other_lbl_tl

    assert lbl not in opened, (lbl, opened)

    flow, dests = nodes[lbl]
    lcl_score = flow * (time_left - 1)
    released = lcl_score

    propogated = False

    opened = frozenset(opened | {lbl})
    for (d, c) in dests:
        if d in opened or d == olbl:
            continue
        propogated = True
        dtl = time_left - 1 - c
        if dtl > 0:
            lbl_tls = ((d, dtl), other_lbl_tl)
            released = max(
                released,
                _dual_traverse(lbl_tls, nodes, max(otl, dtl), opened, states)
                + lcl_score,
            )
    if not propogated and otl > 0:
        # We need to allow the other agent to run
        lbl_tls = (other_lbl_tl, (lbl, -1))
        released = _dual_traverse(lbl_tls, nodes, otl, opened, states) + lcl_score
    return released


def _dual_traverse(lbl_tls, nodes, time_left, opened, states):
    if time_left == 0 or len(opened) == len(nodes):
        return 0

    key = (time_left, lbl_tls, opened)

    if key in states:
        return states[key]

    (lbl1, t1), (lbl2, t2) = lbl_tls

    assert lbl1 != lbl2

    if t1 == t2 == time_left:
        r1 = _dispatch(lbl1, (lbl2, t2), nodes, time_left, opened, states)
        r2 = _dispatch(lbl2, (lbl1, t1), nodes, time_left, opened, states)
        released = max(r1, r2)
    elif t1 == time_left:
        assert t1 > t2
        released = _dispatch(lbl1, (lbl2, t2), nodes, time_left, opened, states)
    elif t2 == time_left:
        assert t2 > t1
        released = _dispatch(lbl2, (lbl1, t1), nodes, time_left, opened, states)
    else:
        raise RuntimeError("should not get here")

    states[key] = released
    key2 = (time_left, lbl_tls[::-1], opened)
    states[key2] = released
    return released


def dual_traverse(graph, time_left):
    """traverse graph within time_limit with two actors

    >>> nodes = simplify(parse_graph(example_text))
    >>> add_paths(nodes)
    >>> dual_traverse(nodes, 26)
    1707
    """
    nodes, opened = setup_nodes(graph)
    released = 0
    _, dests = nodes["AA"]
    with ProcessPoolExecutor() as exe:
        futures = []
        for nd_a, cost_a in dests:
            for nd_b, cost_b in dests:
                if nd_b <= nd_a:
                    continue
                dtls = ((nd_a, time_left - cost_a), (nd_b, time_left - cost_b))
                t = time_left - min(cost_a, cost_b)
                f = exe.submit(_dual_traverse, dtls, nodes, t, opened, states={})
                futures.append(f)
        for f in as_completed(futures):
            released = max(released, f.result())
    return released

    lbl_ts = (("AA", time_left),) * 2
    return _dual_traverse(lbl_ts, nodes, time_left, opened, states={})


if __name__ == "__main__":
    import doctest

    doctest.testmod()
