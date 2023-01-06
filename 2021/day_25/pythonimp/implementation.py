from itertools import count


class Board:
    def __init__(self, board):
        self.board = board
        self.max_i = max(i for ((i, j), c) in board.items())
        self.max_j = max(j for ((i, j), c) in board.items())

    def __repr__(self):
        chunks = []
        for i in range(self.max_i + 1):
            chunks.append("|")
            for j in range(self.max_j + 1):
                c = self.board.get((i, j), ".")
                chunks.append(c)
            chunks.append("|")
            chunks.append("\n")
        return "".join(chunks[:-1])

    def advance(self):
        """
        >>> board = parse(EXAMPLE_TEXT)
        >>> Board(board.advance())
        |....>.>v.>|
        |v.v>.>v.v.|
        |>v>>..>v..|
        |>>v>v>.>.v|
        |.>v.v...v.|
        |v>>.>vvv..|
        |..v...>>..|
        |vv...>>vv.|
        |>.v.v..v.v|
        """

        board = self.board
        new_board = {}
        n_i = self.max_i + 1
        n_j = self.max_j + 1
        for (i, j), c in board.items():
            i1, j1 = (i, j)
            match c:
                case ">":
                    j1 = (j1 + 1) % n_j
                case _:
                    new_board[i1, j1] = c
                    continue
            if (i1, j1) in board:
                i1, j1 = i, j
            new_board[i1, j1] = c

        board = new_board
        new_board = {}

        for (i, j), c in board.items():
            i1, j1 = (i, j)
            match c:
                case "v":
                    i1 = (i1 + 1) % n_i
                case _:
                    new_board[i1, j1] = c
                    continue
            if (i1, j1) in board:
                i1, j1 = i, j
            new_board[i1, j1] = c

        return new_board


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    |v...>>.vv>|
    |.vv>>.vv..|
    |>>.>v>...v|
    |>>v>>.>.v.|
    |v>v.vv.v..|
    |>.>>..v...|
    |.vv..>.>v.|
    |v.v..>>v.v|
    |....v..v.>|
    """
    board = {}
    for i, line in enumerate(text.strip().split("\n")):
        for j, c in enumerate(line):
            if c != ".":
                board[i, j] = c

    return Board(board)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    58
    """
    board = parse(text)
    for i in count():
        new_board = board.advance()
        if new_board == board.board:
            break
        board = Board(new_board)
    return i + 1


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
