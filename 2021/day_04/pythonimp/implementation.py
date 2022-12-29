EXAMPLE_TEXT = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Board:
    def __init__(self, text):
        self.board = board = []
        for line in text.split("\n"):
            board.append([int(x) for x in line.split()])
        self.marks = set()

    def __str__(self):
        lines = []
        for row in self.board:
            lines.append("|" + "".join(f"{x:3}" for x in row) + "|")
        return "\n".join(lines)

    __repr__ = __str__

    def mark(self, x):
        self.marks.add(x)

    def won(self):
        N = len(self.board)
        assert len(self.board[0]) == N
        for row in self.board:
            if sum(x in self.marks for x in row) == N:
                return True
        for i in range(N):
            if sum(x[i] in self.marks for x in self.board) == N:
                return True
        return False

    def score(self, last_mark):
        total = 0
        for row in self.board:
            for x in row:
                if x not in self.marks:
                    total += x
        return total * last_mark


def parse(text):
    """Parse puzzle text into draw and boards

    >>> draws, (b1, b2, b3) = parse(EXAMPLE_TEXT)
    >>> draws[:10]
    [7, 4, 9, 5, 11, 17, 23, 2, 0, 14]
    >>> b2
    |  3 15  0  2 22|
    |  9 18 13 17  5|
    | 19  8  7 25 23|
    | 20 11 10 24  4|
    | 14 21 16 12  6|
    """
    draws, *boards = text.strip().split("\n\n")
    draws = [int(x) for x in draws.split(",")]
    boards = [Board(x) for x in boards]
    return draws, boards


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4512
    """
    draws, boards = parse(text)
    for x in draws:
        for b in boards:
            b.mark(x)
            if b.won():
                return b.score(x)
    raise ValueError()


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1924
    """
    draws, boards = parse(text)
    for x in draws:
        next_rounds_boards = []
        for b in boards:
            b.mark(x)
            if b.won():
                if len(boards) == 1:
                    return boards[0].score(x)
            else:
                next_rounds_boards.append(b)
        boards = next_rounds_boards
    raise ValueError()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
