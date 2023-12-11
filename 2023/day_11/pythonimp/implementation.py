from collections import defaultdict


def parse(text):
    """
    >>> sorted(parse(EXAMPLE_TEXT))
    [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
    """
    board = set()
    for i, row in enumerate(text.strip().split("\n")):
        for j, x in enumerate(row):
            if x == '#':
                board.add((i, j))
    return board


def expand_board(board, expansion=2):
    delta = expansion - 1
    by_row = defaultdict(set)
    for i, j in board:
        by_row[i].add(j)
    max_row = max(by_row)
    offset = 0
    new_board = set()
    for i in range(max_row + 1):
        if i in by_row:
            for j in by_row[i]:
                new_board.add((i + offset, j))
        else:
            offset += delta
    board = new_board

    by_col = defaultdict(set)
    for i, j in board:
        by_col[j].add(i)
    max_col = max(by_col)
    offset = 0
    new_board = set()
    for j in range(max_col + 1):
        if j in by_col:
            for i in by_col[j]:
                new_board.add((i, j + offset))
        else:
            offset += delta
    return new_board


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    374
    """
    board = expand_board(parse(text))
    total = 0
    points = sorted(board)
    for i, (row_1, col_1) in enumerate(points):
        for row_2, col_2 in points[i + 1 :]:
            total += abs(row_2 - row_1) + abs(col_2 - col_1)
    return total


def part_2(text, expansion=1000000):
    """
    >>> part_2(EXAMPLE_TEXT, expansion=10)
    1030
    >>> part_2(EXAMPLE_TEXT, expansion=100)
    8410
    """
    board = expand_board(parse(text), expansion=expansion)
    total = 0
    points = sorted(board)
    for i, (row_1, col_1) in enumerate(points):
        for row_2, col_2 in points[i + 1 :]:
            total += abs(row_2 - row_1) + abs(col_2 - col_1)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
