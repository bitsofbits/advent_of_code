import random
from functools import cache
from itertools import count
from multiprocessing import Pool, cpu_count


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


@cache
def make_tree_from_edges(edges):
    tree = {}
    for a, b in edges:
        tree[a] = a
        tree[b] = b
    return tree


def find_set(F, x):
    parent = F[x]
    if x == parent:
        return x
    node = x
    while parent != node:
        F[node] = parent
        node = parent
        parent = F[node]
    F[x] = parent
    return node


def merge_sets(F, x, y):
    x = find_set(F, x)
    y = find_set(F, y)
    if x != y:
        F[y] = x
        F[x] = x


def karger_contract(edges, forest, remaining_nodes, final_node_count=2):
    # Karger contraction using Kruskal's algorithm

    random.shuffle(edges)
    remaining_edges = []

    for edge in edges:
        (u, v) = edge
        u_root = find_set(forest, u)
        v_root = find_set(forest, v)
        if u_root != v_root:
            if remaining_nodes > final_node_count:
                # Fast version of merge sets given that we have unequal roots
                forest[v_root] = u_root
                remaining_nodes -= 1
            else:
                remaining_edges.append(edge)

    return remaining_edges, forest, remaining_nodes


def contract_wrapper(edges):
    tree = make_tree_from_edges(edges)
    remaining_edges, *_ = karger_contract(list(edges), tree.copy(), len(tree))
    return remaining_edges


def find_min_cuts(edges, n=3):
    edges = tuple(edges)
    with Pool() as pool:
        for cut_edges in pool.imap_unordered(
            contract_wrapper, (edges for _ in count())
        ):
            if len(cut_edges) == n:
                pool.terminate()
                yield cut_edges


def find_nodes(edges):
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    return nodes


def destring_edges(edges):
    node_map = {x: i for i, x in enumerate(sorted(find_nodes(edges)))}
    return list(frozenset([node_map[a], node_map[b]]) for (a, b) in edges)


def count_diconnected(edges):
    edges = destring_edges(edges)
    nodes = find_nodes(edges)
    start, *_ = nodes
    node_set = frozenset(nodes)
    outputs = make_outputs(edges)

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
