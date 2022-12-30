from itertools import count

EXAMPLE_TEXT = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


class Board:
    """
    >>> board = Board(EXAMPLE_TEXT)
    >>> board
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
    """

    def __init__(self, text):
        self.board = self.parse(text)

    @classmethod
    def parse(cls, text):
        board = {}
        for i, line in enumerate(text.strip().split("\n")):
            for j, c in enumerate(line):
                board[i, j] = int(c)
        return board

    def step(self):
        """
        >>> board = Board(EXAMPLE_TEXT)
        >>> board.step()
        0
        >>> board
        6594254334
        3856965822
        6375667284
        7252447257
        7468496589
        5278635756
        3287952832
        7993992245
        5957959665
        6394862637
        >>> board.step()
        35
        >>> board
        8807476555
        5089087054
        8597889608
        8485769600
        8700908800
        6600088989
        6800005943
        0000007456
        9000000876
        8700006848

        """
        flashed = set()
        pending = set()
        for k in self.board:
            self.board[k] += 1
            if k not in flashed and self.board[k] > 9:
                pending.add(k)
        while pending:
            for i, j in pending:
                flashed.add((i, j))
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        k1 = (i + di, j + dj)
                        if k1 in self.board:
                            self.board[k1] += 1
            pending = set()
            for k in self.board:
                if k not in flashed and self.board[k] > 9:
                    pending.add(k)
        for k in flashed:
            self.board[k] = 0
        return len(flashed)

    def __str__(self):
        text = ""
        max_i = max(i for (i, j) in self.board)
        max_j = max(j for (i, j) in self.board)
        for i in range(max_i + 1):
            for j in range(max_j + 1):
                text += str(self.board[i, j])
            text += "\n"
        return text[:-1]

    __repr__ = __str__


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1656
    """
    board = Board(text)
    total = 0
    for _ in range(100):
        total += board.step()
    return total


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    195
    """
    board = Board(text)
    n_jellies = len(board.board)
    for i in count():
        n_flashes = board.step()
        if n_flashes == n_jellies:
            return i + 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
