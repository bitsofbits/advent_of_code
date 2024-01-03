import random


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
            edges.append(((left, right)))
    return edges


def make_outputs(edges, cuts):
    outputs = {}
    for a, b in edges:
        if (a, b) not in cuts:
            if a not in outputs:
                outputs[a] = set()
            outputs[a].add(b)
            if b not in outputs:
                outputs[b] = set()
            outputs[b].add(a)
    return outputs


def make_set(forest, x):
    forest[x] = x


def make_forest_from_edges(edges):
    n = max(max(a, b) for (a, b) in edges) + 1
    # Need at least 16 bit for forest so chose unsigned short.
    forest = [-1] * n
    for a, b in edges:
        forest[a] = a
        forest[b] = b
    return forest


def find_set(forest, node):
    parent = forest[node]
    while parent != node:
        grandparent = forest[parent]
        forest[node] = grandparent
        node = parent
        parent = grandparent
    return node


def merge_sets(forest, x, y):
    x = find_set(forest, x)
    y = find_set(forest, y)
    if x != y:
        forest[y] = x
        forest[x] = x


def karger_contract(edges, forest, remaining_nodes, final_node_count=2):
    # Karger contraction using Kruskal's algorithm
    #
    # Edges and forest are modified. edges are assumed to be pre-shuffled.
    # Need two 16 bit chunks (so 32 bit total) for edges, so chose unsigned long.
    remaining_edges = []
    for edge in edges:
        u_root = find_set(forest, edge & 0xFFFF)
        v_root = find_set(forest, edge >> 16)
        if u_root != v_root:
            if remaining_nodes > final_node_count:
                # Fast version of merge_sets given that we have unequal roots
                forest[v_root] = u_root
                remaining_nodes -= 1
            else:
                remaining_edges.append(edge)
    return remaining_edges, forest, remaining_nodes


def count_edges(graph):
    return len(graph[0])


def karger_stein_contract(edges, forest, node_count):
    # N.B. Input edges and forest are modified. Also, input
    # edges are assumed to be pre-shuffled.

    # In the "real" Karger-Stein algorithm, `target = ceil
    # (1 + remaining_nodes / sqrt(2)), but that takes ~400x as long as,
    # this less aggressive target. This likely related to this graph
    # not being fully connected since the 1/sqrt(2) scaling reduces the
    # edges by 2 each time in a a fully connected graph, while this
    # graph has edges more less proportional to nodes target_nodes.

    target_node_count = min(len(edges) ** 0.5, node_count - 1)
    # target_node_count = node_count // 2

    edges, forest, node_count = karger_contract(
        edges, forest, node_count, target_node_count
    )

    if node_count == 2:
        return edges, forest, node_count

    # We only need to copy and reshuffle on one branch.
    copy_of_edges = edges.copy()
    random.shuffle(copy_of_edges)
    graph_1 = karger_stein_contract(copy_of_edges, forest.copy(), node_count)
    graph_2 = karger_stein_contract(edges, forest, node_count)
    return min([graph_1, graph_2], key=count_edges)


def find_group_sizes(tree):
    group_sizes = {}
    for node, _ in enumerate(tree):
        exemplar = find_set(tree, node)
        if exemplar not in group_sizes:
            group_sizes[exemplar] = 0
        group_sizes[exemplar] += 1
    assert len(group_sizes) == 2
    return tuple(group_sizes.values())


def find_min_cut_sizes(edges, n=3):
    forest = make_forest_from_edges(edges)
    edge_array = []
    for a, b in edges:
        edge_array.append((a << 16) + b)
    n_nodes = len(forest)
    while True:
        random.shuffle(edge_array)
        cut_edge_array, tree, _ = karger_stein_contract(
            edge_array.copy(), forest.copy(), n_nodes
        )

        if len(cut_edge_array) == n:
            return find_group_sizes(tree)


def destring_edges(edges):
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    node_map = {x: i for i, x in enumerate(sorted(nodes))}
    return list((node_map[a], node_map[b]) for (a, b) in edges)


def part_1(text, n_trials=100):
    """
    >>> part_1(EXAMPLE_TEXT)
    54

    inputs -> 532891
    """
    from time import perf_counter

    t0 = perf_counter()
    for _ in range(n_trials):
        edges = destring_edges(parse(text))
        n1, n2 = find_min_cut_sizes(edges)
    seconds_per_trial = (perf_counter() - t0) / n_trials
    print(f"{seconds_per_trial * 1000:.3f} ms per trial over {n_trials} trials")
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

    doctest.testmod()
