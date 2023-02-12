def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ({(1, 0), (0, 2)}, (1, 1))
    """
    board = set()
    for i, row in enumerate(text.strip().split()):
        for j, c in enumerate(row):
            if c == "#":
                board.add((i, j))
    return board, (i // 2, j // 2)


directions = "URDL"


def traverse(board, p, D, steps):
    infections = 0
    D = directions.index(D)
    for _ in range(steps):
        if p in board:
            D = (D + 1) % 4
            board.remove(p)
        else:
            D = (D - 1) % 4
            infections += 1
            board.add(p)
        i, j = p
        match D:
            case 0:
                p = (i - 1, j)
            case 1:
                p = (i, j + 1)
            case 2:
                p = (i + 1, j)
            case 3:
                p = (i, j - 1)
    return infections


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5587
    """
    board, start = parse(text)
    return traverse(board, start, "U", 10000)


states = "CWIF"


def traverse2(board, p, D, steps):
    board = {k: "I" for k in board}
    infections = 0
    D = directions.index(D)
    for _ in range(steps):
        match board.get(p, "C"):
            case "C":
                D = (D - 1) % 4
                board[p] = "W"
            case "W":
                infections += 1
                board[p] = "I"
            case "I":
                D = (D + 1) % 4
                board[p] = "F"
            case "F":
                D = (D + 2) % 4
                del board[p]
        i, j = p
        match D:
            case 0:
                p = (i - 1, j)
            case 1:
                p = (i, j + 1)
            case 2:
                p = (i + 1, j)
            case 3:
                p = (i, j - 1)
    return infections


def part_2(text, count=10_000_000):
    """
    >>> part_2(EXAMPLE_TEXT, 100)
    26
    """
    board, start = parse(text)
    return traverse2(board, start, "U", count)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
