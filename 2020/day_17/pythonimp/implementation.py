from collections import defaultdict


def parse(text):
    """
    >>> len(parse(EXAMPLE_TEXT))
    5
    """
    board = set()
    for i, line in enumerate(text.strip().split("\n")):
        for j, c in enumerate(line):
            if c == "#":
                board.add((i, j, 0))
    return frozenset(board)


def advance(board):
    nbrs = defaultdict(int)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            for dk in [-1, 0, 1]:
                if di == dj == dk == 0:
                    continue
                for i, j, k in board:
                    nbrs[i + di, j + dj, k + dk] += 1
    next_board = set()
    for p in board:
        if nbrs[p] in (2, 3):
            next_board.add(p)
    for p, n in nbrs.items():
        if n == 3:
            next_board.add(p)
    return next_board


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    112
    """
    board = parse(text)
    for _ in range(6):
        board = advance(board)
    return len(board)


def advance4d(board):
    nbrs = defaultdict(int)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            for dk in [-1, 0, 1]:
                for dm in [-1, 0, 1]:
                    if di == dj == dk == dm == 0:
                        continue
                    for i, j, k, m in board:
                        nbrs[i + di, j + dj, k + dk, m + dm] += 1
    next_board = set()
    for p in board:
        if nbrs[p] in (2, 3):
            next_board.add(p)
    for p, n in nbrs.items():
        if n == 3:
            next_board.add(p)
    return next_board


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    848
    """
    board3d = parse(text)
    board = [(*p, 0) for p in board3d]
    for _ in range(6):
        board = advance4d(board)
    return len(board)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
