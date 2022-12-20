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


def simplify(nodes, preserve={"AA"}):
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
            if nd_k.flow == 0 and k not in preserve:
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

    if time_left > 2:
        for (d, c) in dests:
            released = max(
                released,
                _traverse(d, nodes, time_left - c, opened, states),
            )

    if lbl not in opened and time_left > 3:
        opened = frozenset(opened | {lbl})
        for (d, c) in dests:
            released = max(
                released,
                _traverse(d, nodes, time_left - c - 1, opened, states) + lcl_score,
            )

    states[key] = released
    return released


def traverse(graph, time_left):
    """traverse graph within time_limit

    >>> nodes = simplify_AA(parse_graph(example_text))
    >>> traverse(nodes, 30)
    1651
    """
    nodes, opened = setup_nodes(graph)
    return _traverse("AA", nodes, time_left, opened, states={})


def _dispatch(lbl, other_lbl_tl, nodes, time_left, opened, states):
    assert time_left >= 0
    flow, dests = nodes[lbl]
    _, otl = other_lbl_tl

    flow, dests = nodes[lbl]
    lcl_score = flow * (time_left - 1) * (lbl not in opened)
    released = lcl_score

    propped = False

    for (d, c) in dests:
        dtl = time_left - c
        if dtl > 0:
            propped = True
            lbl_tls = ((d, dtl), other_lbl_tl)
            released = max(
                released,
                _dual_traverse(lbl_tls, nodes, max(otl, dtl), opened, states),
            )

    if lbl not in opened:
        opn_copy = None
        for (d, c) in dests:
            dtl = time_left - 1 - c
            if dtl > 0:
                propped = True
                if opn_copy is None:
                    opn_copy = frozenset(opened | {lbl})
                lbl_tls = ((d, dtl), other_lbl_tl)
                released = max(
                    released,
                    _dual_traverse(lbl_tls, nodes, max(otl, dtl), opn_copy, states)
                    + lcl_score,
                )

    if not propped and otl > 0:
        # We need to allow the other agent to run
        lbl_tls = (other_lbl_tl, (lbl, 0))
        released = max(
            released,
            _dual_traverse(lbl_tls, nodes, otl, opened, states) + lcl_score,
        )

    return released


def _dual_traverse(lbl_tls, nodes, time_left, opened, states):
    if time_left == 0 or len(opened) == len(nodes):
        return 0

    key = (time_left, lbl_tls, opened)

    if key in states:
        return states[key]

    (lbl1, t1), (lbl2, t2) = lbl_tls

    if t1 == t2 == time_left and lbl1 != lbl2:
        r1 = _dispatch(lbl1, (lbl2, t2), nodes, time_left, opened, states)
        r2 = _dispatch(lbl2, (lbl1, t1), nodes, time_left, opened, states)
        released = max(r1, r2)
    elif t1 == time_left:
        assert t1 > t2 or (t1 == t2 and lbl1 == lbl2)
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

    >>> nodes = simplify_AA(parse_graph(example_text))
    >>> dual_traverse(nodes, 26)
    1707
    """
    nodes, opened = setup_nodes(graph)
    lbl_ts = (("AA", time_left),) * 2
    return _dual_traverse(lbl_ts, nodes, time_left, opened, states={})


if __name__ == "__main__":
    import doctest

    doctest.testmod()