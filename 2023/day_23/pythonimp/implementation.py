from collections import deque
from multiprocessing import Pool


def render(board, path=()):
    chars = []
    for i, row in enumerate(board):
        for j, x in enumerate(row):
            chars.append('O' if (i, j) in path else x)
        chars.append('\n')
    return ''.join(chars[:-1])


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)))
    #.#####################
    #.......#########...###
    #######.#########.#.###
    ###.....#.>.>.###.#.###
    ###v#####.#v#.###.#.###
    ###.>...#.#.#.....#...#
    ###v###.#.#.#########.#
    ###...#.#.#.......#...#
    #####.#.#.#######.#.###
    #.....#.#.#.......#...#
    #.#####.#.#.#########v#
    #.#...#...#...###...>.#
    #.#.#v#######v###.###v#
    #...#.>.#...>.>.#.###.#
    #####v#.#.###v#.#.###.#
    #.....#...#...#.#.#...#
    #.#########.###.#.#.###
    #...###...#...#...#.###
    ###.###.#.###v#####v###
    #...#...#.#.>.>.#.>.###
    #.###.###.#.###.#.#v###
    #.....###...###...#...#
    #####################.#
    """
    return text.strip().split('\n')


def find_ends(board):
    """
    >>> find_ends(parse(EXAMPLE_TEXT))
    ((0, 1), (22, 21))
    """
    return (0, board[0].index('.')), (len(board) - 1, board[-1].index('.'))


slippery_deltas = {
    '>': [(0, 1)],
    'v': [(1, 0)],
    '<': [(0, -1)],
    '^': [(-1, 0)],
    '.': [(0, 1), (1, 0), (0, -1), (-1, 0)],
}


def part_1(text, max_queue_size=32):
    """
    >>> part_1(EXAMPLE_TEXT, max_queue_size=2)
    94

    input => 2306
    """
    board = parse(text)
    edges, start, end = board_to_graph(board, slippery_deltas)
    return find_longest_path_edges(edges, start, end, max_queue_size=max_queue_size)


boring_deltas = {
    '>': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    'v': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    '<': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    '^': [(0, 1), (1, 0), (0, -1), (-1, 0)],
    '.': [(0, 1), (1, 0), (0, -1), (-1, 0)],
}


def board_to_graph(board, deltas):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> edges, start, end = board_to_graph(board, slippery_deltas)
    >>> start, end
    (1, 527)
    >>> sorted(edges)[:4]
    [(1, 24), (24, 1), (24, 25), (25, 24)]
    """
    start, end = find_ends(board)

    height = len(board)
    width = len(board[0])

    nodes = {
        (i, j): x
        for (i, row) in enumerate(board)
        for (j, x) in enumerate(row)
        if x != '#'
    }

    edges = []
    for (i, j), x in nodes.items():
        for di, dj in deltas.get(x, ()):
            if 0 <= (i1 := i + di) < height and 0 <= (j1 := j + dj) < width:
                if board[i1][j1] != '#':
                    edges.append(((i, j), (i1, j1)))
                    assert (i1, j1) in nodes

    def as_id(i, j):
        return i * width + j

    return (
        frozenset((as_id(*a), as_id(*b)) for (a, b) in edges),
        as_id(*start),
        as_id(*end),
    )


def simplify_edges(edges, start, end):
    nodes = set(x[0] for x in edges) | set(x[1] for x in edges)
    new_edges = [(s, t, 1) for (s, t) in edges]

    inputs = {}
    outputs = {}
    weights = {}
    nodes = set(x[0] for x in new_edges) | set(
        x[1] for x in new_edges
    )  # - {start, end}
    for source, target, weight in new_edges:
        if target not in inputs:
            inputs[target] = set()
        inputs[target].add(source)
        if source not in outputs:
            outputs[source] = set()
        outputs[source].add(target)
        weights[source, target] = weight

    # Reduce all runs of points to single edge
    while True:
        for node in nodes:
            if len(outputs[node]) != len(inputs[node]):
                continue
            assert len(outputs[node]) != 0
            if len(outputs[node]) != 2:
                continue

            for child in outputs[node]:
                for parent in inputs[node]:
                    if child != parent:
                        weights[parent, child] = max(
                            weights.get((parent, child), 0),
                            weights.get((parent, node), 0)
                            + weights.get((node, child), 0),
                        )
                        outputs[parent] = {
                            child if (x == node) else x for x in outputs.get(parent, ())
                        }
                        inputs[child] = {
                            parent if (x == node) else x for x in inputs.get(child, ())
                        }
                        assert node not in outputs[parent]
                        assert node not in inputs[child]
            for child in outputs[node]:
                weights.pop((node, child), 0)
            for parent in inputs[node]:
                weights.pop((parent, node), 0)
            inputs.pop(node)
            outputs.pop(node)
            nodes.remove(node)
            break
        else:
            break

    new_edges = []
    for source, targets in outputs.items():
        for target in targets:
            new_edges.append((source, target, weights[source, target]))

    return new_edges


def path_length(path, weights):
    if not path:
        return 0
    x0 = path[0]
    length = 0
    for x1 in path[1:]:
        length += weights[x0, x1]
        x0 = x1
    return length


def build_initial_state(edges, start, end):
    raw_edges = simplify_edges(edges, start, end)
    raw_nodes = set()
    for a, b, _ in raw_edges:
        raw_nodes.add(a)
        raw_nodes.add(b)
    node_map = {x: 1 << i for (i, x) in enumerate(sorted(raw_nodes))}
    edges = []
    for a, b, w in raw_edges:
        edges.append((node_map[a], node_map[b], w))
    start = node_map[start]
    end = node_map[end]

    source_to_targets = {v: [] for (i, v) in enumerate(node_map.values())}
    for source, target, weight in edges:
        source_to_targets[source].append((target, weight))

    [(adjacent_to_start, start_cost)] = source_to_targets[start]
    [(adjacent_to_end, end_cost)] = source_to_targets[end]

    initial_visited = start | adjacent_to_start
    queue = deque([(start_cost + end_cost, initial_visited, adjacent_to_start)])
    max_length = 0

    return queue, adjacent_to_end, max_length, source_to_targets


def traverse_from_state(state):
    queue, adjacent_to_end, max_length, source_to_targets = state

    while queue:
        path_length, visited, node = queue.pop()
        if node == adjacent_to_end:
            max_length = max(max_length, path_length)
        else:
            for next_node, weight in source_to_targets[node]:
                if not next_node & visited:
                    next_visited = visited | next_node
                    next_path_length = path_length + weight
                    queue.append((next_path_length, next_visited, next_node))
    return max_length


def find_longest_path_edges(edges, start, end, max_queue_size=32):
    state = build_initial_state(edges, start, end)
    queue, *other_state = traverse_warmup_state(state, max_queue_size=max_queue_size)
    args = [(deque([x]),) + tuple(other_state) for x in queue]
    if len(args) == 0:
        return other_state[-2]
    with Pool() as p:
        return max(p.imap_unordered(traverse_from_state, args))


def traverse_warmup_state(state, max_queue_size):
    queue, adjacent_to_end, max_length, source_to_targets = state

    while queue and len(queue) < max_queue_size:
        path_length, visited, node = queue.popleft()
        if node == adjacent_to_end:
            max_length = max(max_length, path_length)
        else:
            for next_node, weight in source_to_targets[node]:
                if not next_node & visited:
                    next_visited = visited | next_node
                    next_path_length = path_length + weight
                    queue.append((next_path_length, next_visited, next_node))
    return queue, adjacent_to_end, max_length, source_to_targets


def part_2(text, max_queue_size=32):
    """
    >>> part_2(EXAMPLE_TEXT, max_queue_size=1)
    154

    inputs -> 6718
    """
    board = parse(text)
    edges, start, end = board_to_graph(board, boring_deltas)
    return find_longest_path_edges(edges, start, end, max_queue_size=max_queue_size)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
