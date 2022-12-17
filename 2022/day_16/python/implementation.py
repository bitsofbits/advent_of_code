import re
from math import inf
from typing import NamedTuple, Tuple

from numba import jit

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
    Node(label='AA', flow=0, dests=('DD', 'II', 'BB'))
    Node(label='BB', flow=13, dests=('CC', 'AA'))
    Node(label='CC', flow=2, dests=('DD', 'BB'))
    Node(label='DD', flow=20, dests=('CC', 'AA', 'EE'))
    Node(label='EE', flow=3, dests=('FF', 'DD'))
    Node(label='FF', flow=0, dests=('EE', 'GG'))
    Node(label='GG', flow=0, dests=('FF', 'HH'))
    Node(label='HH', flow=22, dests=('GG',))
    Node(label='II', flow=0, dests=('AA', 'JJ'))
    Node(label='JJ', flow=21, dests=('II',))
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
            dests = tuple(x.strip() for x in g[2].split(","))
            nodes[lbl] = Node(lbl, flow, dests)
    return nodes


def traverse_from(label, nodes, opened, time_left, states):
    """traverse graph withing time_limit

    >>> nodes = parse_graph(example_text)
    >>> opened = {k for k in nodes if nodes[k].flow == 0}
    >>> traverse_from("AA", nodes, opened, 30, {})
    1651
    """
    if time_left <= 0:
        return 0
    if len(opened) == len(nodes):
        return 0

    state = (time_left, label, frozenset(opened))

    if state in states:
        return states[state]

    nd = nodes[label]
    if label in opened:
        pressure_remaining = 0
    else:
        pressure_remaining = nd.flow * (time_left - 1)

    if time_left < 3:
        # No sense traversing since we can't turn things in on time
        states[state] = pressure_remaining
        return pressure_remaining

    released = pressure_remaining

    for d in nd.dests:
        if time_left > 2:
            released = max(
                released,
                traverse_from(d, nodes, opened, time_left - 1, states),
            )

    if label not in opened:
        opened = opened.copy()
        opened.add(label)
        for d in nd.dests:
            if time_left > 3:
                released = max(
                    released,
                    traverse_from(d, nodes, opened, time_left - 2, states)
                    + pressure_remaining,
                )

    states[state] = released
    return released


def dual_traverse_from(labels, nodes, opened, time_left, states, score, scores):
    """traverse graph withing time_limit

    2176 is too low :-(

    >>> nodes = parse_graph(example_text)
    >>> opened = {k for k in nodes if nodes[k].flow == 0}
    >>> scores = {k : 0 for k in range(0, 27)}
    >>> released = dual_traverse_from(("AA", "AA"), nodes, opened, 26, {}, 0, scores)
    >>> released
    1707
    """
    time_left -= 1
    if time_left <= 0 or len(opened) >= len(nodes):
        return score

    state_key = (time_left, frozenset(labels), frozenset(opened))
    if state_key in states:
        return score + states[state_key]

    lbl1, lbl2 = labels
    nd1, nd2 = nodes[lbl1], nodes[lbl2]
    if time_left == 1:
        # No sense traversing since we can't turn things on in time
        cls1 = lbl1 not in opened
        cls2 = lbl2 not in opened
        remaining = (cls1 * nd1.flow + cls2 * nd2.flow) * time_left
        states[state_key] = remaining
        return remaining

    remaining = [x.flow for (k, x) in nodes.items() if k not in opened]
    remaining.sort(reverse=True)
    max_left = 0
    tl = time_left
    for i, x in enumerate(remaining):
        max_left += x * tl
        if i % 2:
            tl = max(tl - 2, 0)
    if score + max_left <= scores[time_left]:
        return 0  # give up

    scores[time_left] = max(score, scores[time_left])

    released = None
    for d1, opn1 in [(x, False) for x in nd1.dests] + [(lbl1, True)]:
        for d2, opn2 in [(x, False) for x in nd2.dests] + [(lbl2, True)]:

            if (lbl1 == lbl2) and (opn1 is opn2 is True):
                # Can only open a valve once
                continue
            if (opn1 and (lbl1 in opened)) or (opn2 and (lbl2 in opened)):
                # Can only open a valve once
                continue
            lcl_opened = opened.copy()
            if opn1:
                lcl_opened.add(lbl1)
            if opn2:
                lcl_opened.add(lbl2)
            lcl_score = (opn1 * nd1.flow + opn2 * nd2.flow) * time_left
            assert lcl_score >= 0
            new_r = dual_traverse_from(
                (d1, d2),
                nodes,
                opened=lcl_opened,
                time_left=time_left,
                states=states,
                score=score + lcl_score,
                scores=scores,
            )
            if released is None or new_r > released:
                released = new_r

    assert released is not None
    states[state_key] = released - score
    return released


def max_pressure_release(nodes):
    """
    >>> nodes = parse_graph(example_text)
    >>> max_pressure_release(nodes)
    1651
    """
    opened = {k for k in nodes if nodes[k].flow == 0}
    return traverse_from("AA", nodes, opened, 30, {})


def dual_max_pressure_release(nodes):
    """
    >>> nodes = parse_graph(example_text)
    >>> dual_max_pressure_release(nodes)
    1707
    """
    opened = {k for k in nodes if nodes[k].flow == 0}
    scores = {k: 0 for k in range(0, 27)}
    return dual_traverse_from(("AA", "AA"), nodes, opened, 26, {}, 0, scores)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
