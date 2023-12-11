def parse(text):
    """
    >>> board = parse(EXAMPLE_TEXT)
    """
    board = {}
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            board[i, j] = x
    return board


def find_start(board):
    for (i, j), x in board.items():
        if x == 'S':
            return i, j


# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.


def adjacent_to(i, j, board):
    if (i, j) not in board:
        return []
    x = board[i, j]
    if x == '.':
        return []
    if x == 'S':
        raise ValueError("adjaceny undefined for start")
    if x == '|':
        return [(i - 1, j), (i + 1, j)]
    if x == '-':
        return [(i, j + 1), (i, j - 1)]
    if x == 'L':
        return [(i - 1, j), (i, j + 1)]
    if x == 'J':
        return [(i - 1, j), (i, j - 1)]
    if x == '7':
        return [(i + 1, j), (i, j - 1)]
    if x == 'F':
        return [(i + 1, j), (i, j + 1)]
    raise ValueError(x)


def connect(board):
    i0, j0 = find_start(board)
    start_ijs = []
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == dj == 0:
                continue
            i1 = i0 + di
            j1 = j0 + dj
            for i, j in adjacent_to(i1, j1, board):
                if (i, j) == (i0, j0):
                    start_ijs.append((i1, j1))
    assert len(start_ijs) == 2
    # Figure out what shape the start cell is
    start_deltas = set((i - i0, j - j0) for (i, j) in start_ijs)
    if start_deltas == {(1, 0), (-1, 0)}:
        start_pipe = '|'
    elif start_deltas == {(0, 1), (0, -1)}:
        start_pipe = '-'
    elif start_deltas == {(-1, 0), (0, 1)}:
        start_pipe = 'L'
    elif start_deltas == {(-1, 0), (0, -1)}:
        start_pipe = 'J'
    elif start_deltas == {(1, 0), (0, -1)}:
        start_pipe = '7'
    elif start_deltas == {(1, 0), (0, 1)}:
        start_pipe = 'F'
    else:
        raise ValueError(start_deltas)

    #
    start = (i0, j0)
    x0 = start
    x1 = start_ijs[0]
    connections = []
    while x1 != start:
        connections.append(x1)
        [x2] = [x for x in adjacent_to(*x1, board) if x != x0]
        x0 = x1
        x1 = x2

    return (i0, j0), connections, start_pipe


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    8
    """
    board = parse(text)
    start, connections, start_pipe = connect(board)
    return (len(connections) + 1) // 2


def count_inside_locations(board):
    max_i = max(i for (i, j) in board)
    max_j = max(j for (i, j) in board)
    count = 0
    for i in range(max_i + 1):
        is_inside = False
        for j in range(max_j + 1):
            symbol = board.get((i, j), '.')
            if symbol in '7F|':
                is_inside = not is_inside
            elif symbol == '.' and is_inside:
                count += 1
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    10
    """
    board = parse(text)
    start, connections, start_pipe = connect(board)
    new_board = {}
    for k in connections:
        new_board[k] = board[k]
    new_board[start] = start_pipe
    return count_inside_locations(new_board)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()

    doctest.testmod()
