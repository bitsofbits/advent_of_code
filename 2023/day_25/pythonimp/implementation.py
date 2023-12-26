import random
from collections import defaultdict
from copy import deepcopy
from functools import cache
from itertools import permutations
from math import inf, log


def parse(text):
    """
    >>> edges = parse(EXAMPLE_TEXT)
    """
    nodes = []
    edges = []
    lines = text.strip().split('\n')
    lines.sort(key=len)
    for line in lines:
        left, right = line.strip().split(':')
        left = left.strip()
        nodes.append(left)
        for right in right.strip().split():
            nodes.append(right)
            edges.append(frozenset([left, right]))
    return edges


def make_outputs(edges):
    outputs = {}
    for a, b in edges:
        if a not in outputs:
            outputs[a] = set()
        outputs[a].add(b)
        if b not in outputs:
            outputs[b] = set()
        outputs[b].add(a)
    return outputs


def karger_contract(nodes_to_edges, edges, final_vertext_count=2):
    # Karger: https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Could also use Stoer–Wagner

    nodes_to_edges = deepcopy(nodes_to_edges)
    edges = edges.copy()

    while len(nodes_to_edges) > final_vertext_count:
        [target_edge] = random.choices(tuple(edges.keys()), tuple(edges.values()))
        node_1, node_2 = target_edge
        new_node = node_1 | node_2
        assert new_node not in nodes_to_edges
        edges_to_add = defaultdict(int)
        edges_to_remove = set()

        for edge_node in target_edge:
            assert edge_node in nodes_to_edges
            for obsolete_edge in nodes_to_edges[edge_node]:
                node_a, node_b = obsolete_edge
                if obsolete_edge == target_edge:
                    edges_to_remove.add(obsolete_edge)
                elif node_a in target_edge:
                    assert node_b not in target_edge
                    new_edge = frozenset([node_b, new_node])
                    edges_to_add[new_edge] += edges[obsolete_edge]
                    edges_to_remove.add(obsolete_edge)
                elif node_b in target_edge:
                    assert node_a not in target_edge
                    new_edge = frozenset([node_a, new_node])
                    edges_to_add[new_edge] += edges[obsolete_edge]
                    edges_to_remove.add(obsolete_edge)
                else:
                    raise ValueError(obsolete_edge)

        for e, n in edges_to_add.items():
            assert e not in edges
            edges[e] = n
            for nd in e:
                if nd in nodes_to_edges:
                    nodes_to_edges[nd].add(e)
                else:
                    nodes_to_edges[nd] = {e}

        for e in edges_to_remove:
            del edges[e]
            for nd in e:
                nodes_to_edges[nd].remove(e)

        nodes_to_remove = [k for (k, v) in nodes_to_edges.items() if not v]
        for k in nodes_to_remove:
            nodes_to_edges.pop(k)

    return nodes_to_edges, edges


def count_edges(edges):
    return sum(edges.values())


def karger_stein_contract(nodes_to_edges, edges):
    if len(nodes_to_edges) < 6:
        return karger_contract(nodes_to_edges, edges)
    t = 1 + len(nodes_to_edges) / 2**0.5
    G1 = karger_contract(nodes_to_edges, edges, t)
    G2 = karger_contract(nodes_to_edges, edges, t)
    return min(
        karger_stein_contract(*G1),
        karger_stein_contract(*G2),
        key=lambda x: count_edges(x[1]),
    )


@cache
def mangle_edges(edges):
    return {frozenset([frozenset([a]), frozenset([b])]): 1 for (a, b) in edges}


@cache
def make_nodes_to_edges(edges):
    mangled_edges = {frozenset([frozenset([a]), frozenset([b])]): 1 for (a, b) in edges}

    nodes_to_edges = defaultdict(set)
    for edge in mangled_edges:
        a, b = edge
        nodes_to_edges[a].add(edge)
        nodes_to_edges[b].add(edge)
    return dict(nodes_to_edges)


def find_min_cuts(edges, n=3):
    mangled_edges = mangle_edges(edges)
    nodes_to_edges = make_nodes_to_edges(edges)

    _, [(a_nodes, b_nodes)] = karger_stein_contract(nodes_to_edges, mangled_edges)

    choices = (frozenset((a, b)) for a in a_nodes for b in b_nodes)
    choices = (x for x in choices if x in edges)
    return permutations(choices, n)


def find_nodes(edges):
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    return nodes


def destring_edges(edges):
    node_map = {x: i for i, x in enumerate(sorted(find_nodes(edges)))}
    return tuple(frozenset([node_map[a], node_map[b]]) for (a, b) in edges)


def count_diconnected(edges):
    edges = destring_edges(edges)
    nodes = find_nodes(edges)
    start, *_ = nodes
    node_set = frozenset(nodes)
    outputs = make_outputs(edges)
    edges = tuple(edges)

    def traverse(nodes, outputs, start, cuts=()):
        queue = [(start, None)]
        seen = set()
        while queue:
            node, edge = queue.pop()
            if node in seen:
                continue
            seen.add(node)
            for next_node in outputs[node]:
                edge = frozenset((node, next_node))
                if edge not in cuts:
                    queue.append((next_node, edge))
        return len(seen)

    tried = set()
    while True:
        for cuts in find_min_cuts(edges):
            if cuts in tried:
                continue
            print("trying", cuts)
            n = traverse(node_set, outputs, start, cuts=cuts)
            if n < len(nodes):
                return n, len(nodes) - n


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    54

    inputs -> 532891
    """
    edges = parse(text)
    n1, n2 = count_diconnected(edges)
    return n1 * n2


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
