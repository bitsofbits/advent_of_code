from heapq import heappop, heappush


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


def find_longest_path(board, deltas):
    start, end = find_ends(board)
    height = len(board)
    width = len(board[0])
    initial_path = frozenset([start])
    queue = [(-len(initial_path), *start, initial_path)]
    seen = set()
    while queue:
        negative_count, i, j, state = heappop(queue)
        if state in seen:
            continue
        seen.add(state)
        if (i, j) == end:
            continue
        for di, dj in deltas[board[i][j]]:
            next_i = i + di
            next_j = j + dj
            if (
                0 <= next_i < height
                and 0 <= next_j < width
                and board[next_i][next_j] != '#'
            ):
                next_state = state | {(next_i, next_j)}
                heappush(queue, (-len(next_state), next_i, next_j, next_state))
    return max((x for x in seen if end in x), key=len)


def part_1(text, with_graph=True):
    """
    >>> part_1(EXAMPLE_TEXT)
    94
    >>> part_1(EXAMPLE_TEXT, with_graph=True)
    94

    input => 2306
    """
    board = parse(text)
    if with_graph:
        edges, start, end = board_to_graph(board, slippery_deltas)
        return find_longest_path_edges(edges, start, end)
    else:
        path = find_longest_path(board, slippery_deltas)
        return len(path) - 1


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

    def as_id(i, j):
        return i * width + j

    return (
        frozenset((as_id(*a), as_id(*b)) for (a, b) in edges),
        as_id(*start),
        as_id(*end),
    )


def simplify_edges(edges, start, end):
    nodes = set(x[0] for x in edges) | set(x[1] for x in edges)
    edges = [(s, t, 1) for (s, t) in edges]

    new_edges = edges

    inputs = {}
    outputs = {}
    weights = {}
    nodes = (set(x[0] for x in new_edges) | set(x[1] for x in new_edges)) - {start, end}
    for source, target, weight in new_edges:
        if target not in inputs:
            inputs[target] = set()
        inputs[target].add(source)
        if source not in outputs:
            outputs[source] = set()
        outputs[source].add(target)
        weights[source, target] = weight

    while True:
        for node in nodes:
            assert node not in (start, end)
            if len(outputs[node]) != 2 or len(inputs[node]) != 2:
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


def find_longest_path_edges(edges, start, end):
    edges = simplify_edges(edges, start, end)
    initial_visited = frozenset([start])
    queue = [(0, initial_visited, start)]
    max_length = 0
    source_to_targets = {}
    weights = {}
    for source, target, weight in edges:
        if source not in source_to_targets:
            source_to_targets[source] = []
        source_to_targets[source].append(target)
        weights[source, target] = weight
    while queue:
        negative_length, visited, node = queue.pop()
        if node == end:
            max_length = max(max_length, -negative_length)
            continue
        for next_node in source_to_targets[node]:
            if next_node in visited:
                continue
            next_visited = visited | {next_node}
            next_negative_length = negative_length - weights[node, next_node]
            queue.append((next_negative_length, next_visited, next_node))
    return max_length


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    154

    inputs -> 6718
    """
    board = parse(text)
    edges, start, end = board_to_graph(board, boring_deltas)
    return find_longest_path_edges(edges, start, end)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()