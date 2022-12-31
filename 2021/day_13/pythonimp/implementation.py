EXAMPLE_TEXT = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def parse(text):
    """
    >>> dots, folds = parse(EXAMPLE_TEXT)
    >>> print(repr(dots))
    |...#..#..#.|
    |....#......|
    |...........|
    |#..........|
    |...#....#.#|
    |...........|
    |...........|
    |...........|
    |...........|
    |...........|
    |.#....#.##.|
    |....#......|
    |......#...#|
    |#..........|
    |#.#........|
    >>> folds
    [('y', 7), ('x', 5)]
    """
    rawdots, rawfolds = text.strip().split("\n\n")
    dots = []
    for line in rawdots.strip().split("\n"):
        x, y = (int(v) for v in line.strip().split(","))
        dots.append((x, y))
    folds = []
    for line in rawfolds.strip().split("\n"):
        assert line.startswith("fold along ")
        _, _, foldstr = line.split()
        coord, value = foldstr.split("=")
        folds.append((coord, int(value)))
    return set(dots), folds


def repr(board):
    max_x = max(x for (x, y) in board)
    # note Y increases downward
    max_y = max(y for (x, y) in board)
    text = ""
    for i in range(max_y + 1):
        text += "|"
        for j in range(max_x + 1):
            if (j, i) in board:
                text += "#"
            else:
                text += "."
        text += "|\n"
    return text[:-1]


def fold_x(board, x0):
    new_board = set()
    for x, y in board:
        if x > x0:
            x = 2 * x0 - x
        new_board.add((x, y))
    return new_board


def fold_y(board, y0):
    new_board = set()
    for x, y in board:
        if y > y0:
            y = 2 * y0 - y
        new_board.add((x, y))
    return new_board


def fold(board, coord, value):
    match coord:
        case "x":
            return fold_x(board, value)
        case "y":
            return fold_y(board, value)
    raise ValueError()


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    17
    """
    board, folds = parse(text)
    board = fold(board, *folds[0])
    return len(board)


def part_2(text):
    """
    >>> print(part_2(EXAMPLE_TEXT))
    |#####|
    |#...#|
    |#...#|
    |#...#|
    |#####|
    """
    board, folds = parse(text)
    for coord, val in folds:
        board = fold(board, coord, val)
    return repr(board)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
