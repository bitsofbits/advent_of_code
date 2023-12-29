import random
from itertools import permutations
from math import ceil


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


def random_pick(remaining_edges, W, adjacency):
    # See: https://people.engr.tamu.edu/j-chen3/courses/658/2016/notes/s1.pdf
    n_nodes = len(W)
    t = random.randrange(remaining_edges) + 1
    i = 0
    w = W[0]
    while t > w:
        i += 1
        w += W[i]
    w -= W[i]
    t = t - w
    j = i
    while t > 0:
        j += 1
        t -= adjacency[i * n_nodes + j]

    return i, j


def karger_contract(
    remaining_nodes,
    remaining_edges,
    W,
    nodes,
    adjacency,
    final_node_count=2,
):
    # Karger: https://en.wikipedia.org/wiki/Karger%27s_algorithm
    # Could also use Stoer–Wagner -- faster, but maybe harder to implement

    n_nodes = len(nodes)

    while remaining_nodes > final_node_count:
        i, j = random_pick(remaining_edges, W, adjacency)

        assert i < j

        # All the edges associates with i are moved to
        # point to new node, now at i
        nodes[i] = nodes[i] | nodes[j]

        # Add all the edges associates with j
        for n in range(i):
            adjacency[n * n_nodes + i] += adjacency[n * n_nodes + j]
            W[n] += adjacency[n * n_nodes + j]
        for n in range(i + 1, j):
            adjacency[i * n_nodes + n] += adjacency[n * n_nodes + j]
            W[i] += adjacency[n * n_nodes + j]
        for n in range(j, n_nodes):
            adjacency[i * n_nodes + n] += adjacency[j * n_nodes + n]
            W[i] += adjacency[j * n_nodes + n]

        # Delete edges associated with j
        nodes[j] = None
        remaining_nodes -= 1
        remaining_edges -= adjacency[i * n_nodes + j]
        for n in range(j):
            W[n] -= adjacency[n * n_nodes + j]
            adjacency[n * n_nodes + j] = 0
        for n in range(j, n_nodes):
            W[j] -= adjacency[j * n_nodes + n]
            adjacency[j * n_nodes + n] = 0

    valid_indices = [i for i in range(n_nodes) if nodes[i] is not None]

    W = [W[i] for i in valid_indices]
    nodes = [nodes[i] for i in valid_indices]
    adjacency = [
        adjacency[i * n_nodes + j] for i in valid_indices for j in valid_indices
    ]

    return remaining_nodes, remaining_edges, W, nodes, adjacency


def build_karger_args(edges):
    def wrap(node):
        return frozenset({node})

    nodes = set()
    for i, (node_a, node_b) in enumerate(edges):
        nodes.add(wrap(node_a))
        nodes.add(wrap(node_b))
    nodes = sorted(nodes)
    remaining_nodes = n_nodes = len(nodes)
    node_map = {k: i for (i, k) in enumerate(nodes)}

    # We only use (and fill in) the upper diagonal
    adjacency = [0] * (n_nodes**2)
    W = [0] * n_nodes
    remaining_edges = 0
    for node_a, node_b in edges:
        i = node_map[wrap(node_a)]
        j = node_map[wrap(node_b)]
        assert i != j
        if i > j:
            i, j = j, i
        adjacency[i * n_nodes + j] += 1
        remaining_edges += 1
        W[i] += 1

    return remaining_nodes, remaining_edges, W, nodes, adjacency


def count_edges(edges):
    return sum(edges.values())


def count_nodes(edges):
    nodes = set()
    for i, (node_a, node_b) in enumerate(edges):
        nodes.add(node_a)
        nodes.add(node_b)
    return len(nodes)


def build_edges_from_adjacency(adjacency, nodes):
    n_nodes = len(nodes)
    edges = {}
    for i, node_a in enumerate(nodes):
        for j, node_b in enumerate(nodes):
            if j > i:
                count = adjacency[i * n_nodes + j]
                # assert count == adjacency[j * n_nodes + i]
                if count:
                    if node_a != node_b:
                        e = frozenset([node_a, node_b])
                        assert len(e) == 2
                        edges[e] = count
                    assert None not in (node_a, node_b)
    return edges


def karger_stein_contract(remaining_nodes, remaining_edges, W, nodes, adjacency):
    if remaining_nodes <= 6:
        return karger_contract(remaining_nodes, remaining_edges, W, nodes, adjacency)
    t = ceil(1 + remaining_nodes / 2**0.5)
    G1 = karger_contract(
        remaining_nodes, remaining_edges, W.copy(), nodes.copy(), adjacency.copy(), t
    )
    G2 = karger_contract(remaining_nodes, remaining_edges, W, nodes, adjacency, t)
    return min(
        karger_stein_contract(*G1),
        karger_stein_contract(*G2),
        key=lambda x: x[1],
    )


def find_min_cuts(edges, n=3):
    karger_args = build_karger_args(edges)
    *_, nodes, adjacency = karger_stein_contract(*karger_args)
    [(a_nodes, b_nodes)] = build_edges_from_adjacency(adjacency, nodes)

    choices = (frozenset((a, b)) for a in a_nodes for b in b_nodes)
    choices = (x for x in choices if x in edges)
    for x in permutations(choices, n):
        yield frozenset(x)


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
