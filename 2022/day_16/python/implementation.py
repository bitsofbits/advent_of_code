import re
from math import inf
from typing import NamedTuple, Tuple

# def simplify_A(nodes):
#     """
#     >>> nodes = simplify_A(parse_graph(example_text))
#     >>> for k in sorted(nodes): print(nodes[k])
#     Node(label='AA', flow=0, dests=(('BB', 1), ('DD', 1), ('JJ', 2)))
#     Node(label='BB', flow=13, dests=(('CC', 1), ('DD', 4), ('JJ', 3)))
#     Node(label='CC', flow=2, dests=(('BB', 1), ('DD', 1)))
#     Node(label='DD', flow=20, dests=(('BB', 4), ('CC', 1), ('EE', 1), ('JJ', 3)))
#     Node(label='EE', flow=3, dests=(('DD', 1), ('HH', 3)))
#     Node(label='HH', flow=22, dests=(('EE', 3),))
#     Node(label='JJ', flow=21, dests=(('BB', 3), ('DD', 3)))
#     """
#     s1 = simplify(nodes, preserve={"AA"})
#     s2 = simplify(nodes, preserve=())
#     s2["AA"] = s1["AA"]
#     return s2


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
            dests = tuple(set(x.strip() for x in g[2].split(",")))
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
        dests = set((d, 1) for d in nd.dests)
        nodes[k] = Node(nd.label, nd.flow, dests)
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
                        if d == p:
                            continue
                        cd = c + c0
                        if d in new_dests:
                            cd = min(cd, new_dests[d])
                        new_dests[d] = cd
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


def simplify_A(nodes):
    """
    >>> nodes = simplify_A(parse_graph(example_text))
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=(('BB', 1), ('DD', 1), ('JJ', 2)))
    Node(label='BB', flow=13, dests=(('CC', 1), ('DD', 4), ('JJ', 3)))
    Node(label='CC', flow=2, dests=(('BB', 1), ('DD', 1)))
    Node(label='DD', flow=20, dests=(('BB', 4), ('CC', 1), ('EE', 1), ('JJ', 3)))
    Node(label='EE', flow=3, dests=(('DD', 1), ('HH', 3)))
    Node(label='HH', flow=22, dests=(('EE', 3),))
    Node(label='JJ', flow=21, dests=(('BB', 3), ('DD', 3)))
    """
    s1 = simplify(nodes, preserve={"AA"})
    s2 = simplify(nodes, preserve=())
    s2["AA"] = s1["AA"]
    return s2


def stretch(nodes):
    """stretch simplified graph by adding dummy nodes

    >>> nodes = stretch(simplify(parse_graph(example_text)))
    >>> for k in sorted(nodes): print(nodes[k])
    Node(label='AA', flow=0, dests=('AAJJ1', 'BB', 'DD'))
    Node(label='AAJJ1', flow=0, dests=('JJ',))
    Node(label='BB', flow=13, dests=('AA', 'CC'))
    Node(label='CC', flow=2, dests=('BB', 'DD'))
    Node(label='DD', flow=20, dests=('AA', 'CC', 'EE'))
    Node(label='EE', flow=3, dests=('DD', 'EEHH1'))
    Node(label='EEHH1', flow=0, dests=('EEHH2',))
    Node(label='EEHH2', flow=0, dests=('HH',))
    Node(label='HH', flow=22, dests=('HHEE1',))
    Node(label='HHEE1', flow=0, dests=('HHEE2',))
    Node(label='HHEE2', flow=0, dests=('EE',))
    Node(label='JJ', flow=21, dests=('JJAA1',))
    Node(label='JJAA1', flow=0, dests=('AA',))
    """
    nodes = nodes.copy()
    # Convert to new format?
    for k in list(nodes):
        nd_k = nodes[k]
        new_dests = set()
        for d, c in nd_k.dests:
            if c == 1:
                new_dests.add(d)
            else:
                k1 = f"{k}{d}{1}"
                new_dests.add(k1)
                for i in range(1, c - 1):
                    k2 = f"{k}{d}{i + 1}"
                    nodes[k1] = Node(k1, 0, {k2})
                    k1 = k2
                nodes[k1] = Node(k1, 0, {d})
        nodes[k] = Node(nd_k.label, nd_k.flow, new_dests)
    for k in list(nodes):
        nd = nodes[k]
        assert nd.label == k
        dests = tuple(sorted(nd.dests))
        nodes[k] = Node(nd.label, nd.flow, dests)
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


class UpperBound(int):
    pass


def upper_bound(time_left, lbl1, lbl2, nodes, opened):
    remaining = [x.flow for (k, x) in nodes.items() if k not in opened]
    remaining.sort(reverse=True)
    return sum(
        x * max(time_left - 2 * i, 0) for (i, x) in enumerate(remaining[0::2])
    ) + sum(x * max(time_left - 2 * i, 0) for (i, x) in enumerate(remaining[1::2]))


def dual_traverse_from(labels, nodes, opened, time_left, states, score, scores):
    """traverse graph withing time_limit

    # >>> nodes = parse_graph(example_text)
    # >>> opened = {k for k in nodes if nodes[k].flow == 0}
    # >>> scores = {k : 0 for k in range(0, 27)}
    # >>> released = dual_traverse_from(("AA", "AA"), nodes, opened, 26, {}, 0, scores)
    # >>> released
    # 1707
    """
    time_left -= 1
    if time_left < 0:
        return score
    scores[time_left] = max(score, scores[time_left])

    state_key = (time_left, frozenset(labels), frozenset(opened))
    if state_key in states:
        remaining = states[state_key]
        if isinstance(remaining, UpperBound):
            if score + remaining < scores[time_left]:
                return UpperBound(score + remaining)
        else:
            return score + remaining

    lbl1, lbl2 = labels
    nd1, nd2 = nodes[lbl1], nodes[lbl2]
    # if time_left == 1:
    #     # No sense traversing since we can't turn things on in time
    #     cls1 = lbl1 not in opened
    #     cls2 = lbl2 not in opened
    #     remaining = (cls1 * nd1.flow + cls2 * nd2.flow) * time_left
    #     states[state_key] = remaining
    #     return remaining

    max_left = upper_bound(time_left, lbl1, lbl2, nodes, opened)
    if score + max_left < scores[time_left]:
        # No way to get the best score, so give up
        states[state_key] = UpperBound(max_left)
        return UpperBound(score + max_left)

    released = 0
    for d1, opn1 in [(x, False) for x in nd1.dests] + [(lbl1, True)]:
        for d2, opn2 in [(x, False) for x in nd2.dests] + [(lbl2, True)]:

            if lbl1 == lbl2 and opn1 is opn2 is True:
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
            if new_r > released:
                released = new_r

    if isinstance(released, UpperBound):
        states[state_key] = UpperBound(released - score)
    else:
        states[state_key] = released - score
    return released


def dual_traverse(graph, start, max_time):
    """
    # >>> nodes = parse_graph(example_text)
    # >>> released = dual_traverse(nodes, ("AA", "AA"), 26)
    # >>> released
    """
    # Process nodes into simpler form
    fast_nodes = {}
    for k, nd in graph.items():
        fast_nodes[k] = tuple((d, 0) for d in nd.dests) + ((k, nd.flow),)

    k1, k2 = start
    assert k1 == "AA" and k2 == "AA"
    stack = [(max_time, k1, k2, 0, fast_nodes)]
    states = {}
    max_score = 0
    while stack:
        time_left, k1, k2, score, nodes = stack.pop()
        state_key = (time_left, k1, k2, tuple(sorted(nodes.items())))
        states[state_key] = score  # how to get this into a useful form
        max_score = max(score, max_score)
        time_left -= 1
        if time_left == 0:
            continue
        for d1, flow_1 in nodes[k1]:
            for d2, flow_2 in nodes[k2]:
                if flow_1 != 0 or flow_2 != 0:
                    nodes = nodes.copy()
                    if flow_1 != 0:
                        nodes[k1] = tuple(
                            (dx, 0 if dx == d1 else fx) for (dx, fx) in nodes[k1]
                        )
                    if flow_2 != 0:
                        nodes[k2] = tuple(
                            (dx, 0 if dx == d1 else fx) for (dx, fx) in nodes[k2]
                        )
                next_score = score + (flow_1 + flow_2) * time_left
                stack.append((time_left, d1, d2, next_score, nodes))
    return max_score


def max_pressure_release(nodes):
    """
    >>> nodes = parse_graph(example_text)
    >>> max_pressure_release(nodes)
    1651
    """
    nodes = stretch(simplify(nodes))
    opened = {k for k in nodes if nodes[k].flow == 0}
    return traverse_from("AA", nodes, opened, 30, {})


def dual_max_pressure_release(nodes):
    """
    # >>> nodes = parse_graph(example_text)
    # >>> dual_max_pressure_release(nodes)
    # 1707
    """
    nodes = stretch(simplify(nodes))
    opened = {k for k in nodes if nodes[k].flow == 0}
    scores = {k: 0 for k in range(0, 27)}
    released = dual_traverse_from(("AA", "AA"), nodes, opened, 26, {}, 0, scores)
    assert not isinstance(released, UpperBound)
    return released


if __name__ == "__main__":
    import doctest

    doctest.testmod()
