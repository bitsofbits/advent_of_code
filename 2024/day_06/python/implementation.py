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


def move(guard, board):
    i, j, d = guard
    di, dj = unit_vectors[d]
    i1, j1 = (i + di, j + dj)
    if (i1, j1) in board:
        # blocked
        return (i, j, clockwise[d])
    else:
        return (i1, j1, d)


def find_path(board, shape, guard):
    states = set()
    while True:
        if not on_board(guard, shape):
            status = 'exited'
            break
        if guard in states:
            status = 'looped'
            break
        states.add(guard)
        guard = move(guard, board)
    path = {x[:2] for x in states}
    return path, status


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    41
    """
    board, shape, guard = parse(text)
    path, _ = find_path(board, shape, guard)
    return len(path)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    6
    """
    board, shape, guard = parse(text)
    default_path, _ = find_path(board, shape, guard)
    loop_count = 0
    for x in default_path:
        _, status = find_path(board | {x}, shape, guard)
        if status == 'looped':
            loop_count += 1
    return loop_count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
