from itertools import count


class Board:
    def __init__(self, board):
        self.east = {loc for (loc, c) in board.items() if c == ">"}
        self.south = {loc for (loc, c) in board.items() if c == "v"}
        self.max_i = max(i for ((i, j), c) in board.items())
        self.max_j = max(j for ((i, j), c) in board.items())

    def __repr__(self):
        chunks = []
        for i in range(self.max_i + 1):
            chunks.append("|")
            for j in range(self.max_j + 1):
                if (i, j) in self.east:
                    c = ">"
                elif (i, j) in self.south:
                    c = "v"
                else:
                    c = "."
                chunks.append(c)
            chunks.append("|")
            chunks.append("\n")
        return "".join(chunks[:-1])

    def advance(self):
        """
        >>> board = parse(EXAMPLE_TEXT)
        >>> board.advance()
        False
        >>> board
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
        east = self.east
        south = self.south
        n_i = self.max_i + 1
        n_j = self.max_j + 1

        static = True
        new_east = set()
        for i, j in east:
            j1 = (j + 1) % n_j
            if (i, j1) in south or (i, j1) in east:
                new_east.add((i, j))
            else:
                static = False
                new_east.add((i, j1))

        new_south = set()
        for i, j in south:
            i1 = (i + 1) % n_i
            if (i1, j) in south or (i1, j) in new_east:
                new_south.add((i, j))
            else:
                static = False
                new_south.add((i1, j))

        self.south = new_south
        self.east = new_east

        return static


def parse(text):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> board
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
    for i in count(1):
        if board.advance():
            return i


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
