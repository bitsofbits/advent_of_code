import random
from collections import defaultdict
from functools import cache
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
    F[x] = x


def find_set(F, x):
    root = F[x]
    if x == root:
        return x
    while (next_root := F[root]) != root:
        root = next_root
    F[x] = root
    return root


def merge_sets(F, x, y):
    x = find_set(F, x)
    y = find_set(F, y)
    if x != y:
        F[y] = x
        F[x] = x


@cache
def build_kruskal_args(edges):
    forest = {}
    nodes = find_nodes(edges)
    remaining_nodes = len(nodes)
    forest = {}
    for node in nodes:
        make_set(forest, node)
    return list(edges), forest, remaining_nodes


def kruskal(edges, forest, remaining_nodes):
    # Karger contraction using Kruskal's algorithm

    random.shuffle(edges)
    remaining_edges = []

    for i, edge in enumerate(edges):
        (u, v) = edge
        u_root = find_set(forest, u)
        v_root = find_set(forest, v)
        if u_root != v_root:
            if remaining_nodes <= 2:
                remaining_edges.append(edge)
            else:
                merge_sets(forest, u_root, v_root)
                remaining_nodes -= 1

    return remaining_edges, forest, remaining_nodes


def kurskal_wrapper(edges):
    edges, forest, remaining_nodes = build_kruskal_args(edges)
    remaining_edges, *_ = kruskal(edges.copy(), forest.copy(), remaining_nodes)
    return remaining_edges


def find_min_cuts(edges, repeats=128, n=3):
    used = set()
    counts = defaultdict(int)
    with Pool() as pool:
        while True:
            for cut_edges in pool.imap_unordered(kurskal_wrapper, [edges] * repeats):
                for x in permutations(cut_edges, n):
                    counts[x] += 1
            value = max(counts, key=lambda x: counts[x] * (x not in used))
            used.add(value)
            yield value


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

    def traverse(nodes, outputs, start):
        queue = [start]
        seen = set()
        while queue:
            node = queue.pop()
            seen.add(node)
            for next_node in outputs[node]:
                if next_node not in seen:
                    seen.add(node)
                    edge = frozenset((node, next_node))
                    if edge not in cuts:
                        queue.append(next_node)
        return len(seen)

    tried = set()
    for cuts in find_min_cuts(edges):
        cuts = frozenset(cuts)
        if cuts in tried:
            continue
        pruned_outputs = {k: v - cuts for (k, v) in outputs.items()}
        n = traverse(node_set, pruned_outputs, start)
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
