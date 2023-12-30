import random
from collections import defaultdict
from itertools import permutations
from multiprocessing import Pool


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


def make_set(F, x):
    # root, sub-root, size
    F[x] = (x, 1)


def find_set(F, x):
    root, size = F[x]
    if root == x:
        return x
    else:
        root = find_set(F, root)
        F[x] = (root, size)
        return root


def merge_sets(F, x, y):
    _, x_size = F[x]
    _, y_size = F[y]
    x = find_set(F, x)
    y = find_set(F, y)
    if x == y:
        return
    if x_size < y_size:
        x, y = y, x
        x_size, y_size = y_size, x_size

    F[y] = (x, y_size)
    F[x] = (x, x_size + y_size)


def extract_kruskal_sets(forest):
    sets = defaultdict(set)
    for node in forest:
        sets[find_set(forest, node)].add(node)
    return list(sets.values())


# -        remaining_edges -= adjacency[i * n_nodes + j]


def build_kruskal_args(edges):
    forest = {}
    nodes = find_nodes(edges)
    remaining_nodes = len(nodes)
    forest = {}
    for node in nodes:
        make_set(forest, node)
    return list(edges), forest, remaining_nodes


def kruskal(edges, forest, remaining_nodes, final_node_count=2):
    # Karger contraction using Kruskal's algorithm

    random.shuffle(edges)
    remaining_edges = []

    for i, edge in enumerate(edges):
        (u, v) = edge
        u_root = find_set(forest, u)
        v_root = find_set(forest, v)
        if u_root != v_root:
            if remaining_nodes <= final_node_count:
                remaining_edges.append(edge)
            else:
                merge_sets(forest, u_root, v_root)
                remaining_nodes -= 1

    return remaining_edges, forest, remaining_nodes


# def count_forest_edges(args):
#     forest, n_nodes, edges = args
#     return len(edges)


# # This isn't working with kruskal contraction -- probably because I'm not counting the number of
# # edges incorectly.
# def karger_stein_contract(edges, forest, remaining_nodes):
#     if remaining_nodes <= 6:
#         return kruskal(edges, forest, remaining_nodes)
#     t = ceil(1 + remaining_nodes / 2**0.5)
#     G1 = kruskal(edges.copy(), forest.copy(), remaining_nodes, t)
#     G2 = kruskal(edges.copy(), forest.copy(), remaining_nodes, t)
#     return min(
#         karger_stein_contract(*G1), karger_stein_contract(*G2), key=lambda x: len(x[0])
#     )


def kurskal_wrapper(arg):
    edges, forest, remaining_nodes = arg
    return kruskal(edges.copy(), forest.copy(), remaining_nodes)


def find_min_cuts(edges, repeats=32, n=3):
    edges, forest, remaining_nodes = build_kruskal_args(edges)

    args = [(edges, forest, remaining_nodes)] * repeats
    used = set()
    with Pool() as pool:
        counts = defaultdict(int)
        while True:
            for remaining_edges, *_ in pool.imap_unordered(kurskal_wrapper, args):
                for x in permutations(remaining_edges, n):
                    counts[x] += 1
            value = max(counts, key=lambda x: counts[x] * (x not in used))
            used.add(value)
            yield value

    # # karger_stein_contract(*args)
    # choices = edges
    # # (a_nodes, b_nodes) = extract_kruskal_sets(forest)
    # # choices = edges
    # # choices = (frozenset((a, b)) for a in a_nodes for b in b_nodes)
    # # choices = (x for x in choices if x in edges)
    # for x in permutations(choices, n):
    #     yield frozenset(x)


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
    for cuts in find_min_cuts(edges):
        if cuts in tried:
            continue
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
