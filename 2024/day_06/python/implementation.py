def parse(text):
    """
    >>> board, shape, guard = parse(EXAMPLE_TEXT)
    >>> shape
    (10, 10)
    >>> guard
    (6, 4, '^')
    """
    board = set()
    for i, line in enumerate(text.strip().split('\n')):
        for j, x in enumerate(line):
            if x == '.':
                pass
            elif x == '#':
                board.add((i, j))
            elif x in '><^v':
                guard = (i, j, x)
            else:
                raise ValueError((i, j, x))
    shape = (i + 1, j + 1)
    return frozenset(board), shape, guard


def on_board(guard, shape):
    i, j, _ = guard
    m, n = shape
    return 0 <= i < m and 0 <= j < n


unit_vectors = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

clockwise = {k: v for (k, v) in zip('^>v<', '>v<^')}


def make_edge_states(shape):
    m, n = shape
    states = {}
    for d in '^>v<':
        for i in range(m):
            states[(i, -1, d)] = 'exited'
            states[(i, n, d)] = 'exited'
        for j in range(n):
            states[(-1, j, d)] = 'exited'
            states[(m, j, d)] = 'exited'
    return states


def move(guard, board):
    i, j, d = guard
    di, dj = unit_vectors[d]
    i1, j1 = (i + di, j + dj)
    if (i1, j1) in board:
        # blocked
        return (i, j, clockwise[d])
    else:
        return (i1, j1, d)


def find_path(board, shape, guard, states=None):
    path = []
    if states is None:
        states = make_edge_states(shape)
    else:
        states = states.copy()
    while True:
        if guard in states:
            return path, states[guard]
        path.append(guard)
        states[guard] = 'looped'
        guard = move(guard, board)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    41
    """
    board, shape, guard = parse(text)
    path, _ = find_path(board, shape, guard)
    return len({x[:2] for x in path})


def find_path_fast(board, shape, guard, states):
    # Find the path, but don't track path for extra speed
    states = states.copy()
    i, j, d = guard
    cw = clockwise
    while True:
        guard = (i, j, d)
        if guard in states:
            return states[guard]
        states[guard] = 'looped'
        di, dj = unit_vectors[d]
        i1, j1 = (i + di, j + dj)
        if (i1, j1) in board:
            d = cw[d]
        else:
            i, j = i1, j1


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    6
    """
    board, shape, guard = parse(text)
    path, _ = find_path(board, shape, guard)
    loop_count = 0
    states = make_edge_states(shape)
    tried = set()
    last_x = path[0]
    for i, x in enumerate(path[1:]):
        location = x[:2]
        if location in tried:
            continue
        tried.add(location)
        status = find_path_fast(board | {location}, shape, last_x, states)
        states[last_x] = 'looped'
        loop_count += status == 'looped'
        last_x = x
    return loop_count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
