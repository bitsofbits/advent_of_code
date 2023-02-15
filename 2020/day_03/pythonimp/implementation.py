def parse(text):
    """
    >>> H, W, board = parse(EXAMPLE_TEXT)
    >>> H, W, len(board)
    (11, 11, 37)
    """
    board = set()
    for i, line in enumerate(text.strip().split("\n")):
        for j, c in enumerate(line):
            if c == "#":
                board.add((i, j))
    return i + 1, j + 1, frozenset(board)


def count_trees(H, W, board, slope):
    i = j = 0
    trees = 0
    dj, di = slope
    while i < H:
        if (i, j) in board:
            trees += 1
        i += di
        j = (j + dj) % W
    return trees


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7
    """
    H, W, board = parse(text)
    return count_trees(H, W, board, slope=(3, 1))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    336
    """
    H, W, board = parse(text)
    product = 1
    for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        product *= count_trees(H, W, board, slope=slope)
    return product


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
