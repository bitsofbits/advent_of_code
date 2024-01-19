from collections import defaultdict


def render(board):
    rows = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append('#' if ((i, j) in board) else '•')
        rows.append(''.join(row))
    return '\n'.join(rows)


def render2(board, z=0):
    rows = []
    assert (z, 2, 2) not in board
    for i in range(5):
        row = []
        for j in range(5):
            if i == j == 2:
                row.append('?')
            else:
                row.append('#' if ((z, i, j) in board) else '•')
        rows.append(''.join(row))
    return '\n'.join(rows)


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)))
    ••••#
    #••#•
    #••##
    ••#••
    #••••
    """
    board = set()
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            if x == '#':
                board.add((i, j))
    return frozenset(board)


def compute_next_board(board):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> board = compute_next_board(board)
    >>> print(render(board))
    #••#•
    ####•
    ###•#
    ##•##
    •##••
    """
    adjacent = defaultdict(int)
    for i, j in board:
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            adjacent[i + di, j + dj] += 1

    next_board = set()
    for loc, cnt in adjacent.items():
        i, j = loc
        if not (0 <= i < 5 and 0 <= j < 5):
            continue
        if loc in board:
            if cnt == 1:
                next_board.add(loc)
        elif cnt in (1, 2):
            next_board.add(loc)

    return frozenset(next_board)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2129920
    """
    board = parse(text)
    seen = {board}
    while True:
        board = compute_next_board(board)
        if board in seen:
            return sum(2 ** (5 * i + j) for (i, j) in board)
        seen.add(board)


def compute_next_recursive_board(board):
    """
    >>> base_board = parse(EXAMPLE_TEXT)
    >>> board = frozenset((0, i, j) for (i, j) in base_board)
    >>> for _ in range(10):
    ...     board = compute_next_recursive_board(board)
    >>> print(render2(board))
    •#•••
    •#•##
    •#?••
    •••••
    •••••
    """
    adjacent = defaultdict(int)
    for z0, i0, j0 in board:
        for di, dj in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            i = i0 + di
            j = j0 + dj
            match (i, j):
                case (2, 2):
                    match (i0, j0):
                        case (1, _):
                            for j1 in range(5):
                                adjacent[z0 + 1, 0, j1] += 1
                        case (3, _):
                            for j1 in range(5):
                                adjacent[z0 + 1, 4, j1] += 1
                        case (_, 1):
                            for i1 in range(5):
                                adjacent[z0 + 1, i1, 0] += 1
                        case (_, 3):
                            for i1 in range(5):
                                adjacent[z0 + 1, i1, 4] += 1
                case (-1, _):
                    adjacent[z0 - 1, 1, 2] += 1
                case (5, _):
                    adjacent[z0 - 1, 3, 2] += 1
                case (_, -1):
                    adjacent[z0 - 1, 2, 1] += 1
                case (_, 5):
                    adjacent[z0 - 1, 2, 3] += 1
                case (_, _):
                    adjacent[z0, i, j] += 1

    next_board = set()
    for loc, cnt in adjacent.items():
        z, i, j = loc
        assert 0 <= i < 5 and 0 <= j < 5, loc
        if loc in board:
            if cnt == 1:
                next_board.add(loc)
        elif cnt in (1, 2):
            next_board.add(loc)

    return frozenset(next_board)


def part_2(text, minutes=200):
    """
    >>> part_2(EXAMPLE_TEXT, minutes=10)
    99
    """
    base_board = parse(text)
    board = frozenset((0, i, j) for (i, j) in base_board)
    for _ in range(minutes):
        board = compute_next_recursive_board(board)
    return len(board)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
