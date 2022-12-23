from collections import defaultdict, deque
from sys import maxsize

example_text = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""


class Board:
    """
    >>> board = Board(example_text)
    >>> print(board)
    |....#..|
    |..###.#|
    |#...#.#|
    |.#...##|
    |#.###..|
    |##.#.##|
    |.#..#..|
    """

    def __init__(self, text):
        self.initial_board = self.parse(text)
        self.reset()

    def reset(self):
        self.board = self.initial_board.copy()
        self.moves = deque(
            [
                ((-1, -1), (-1, 0), (-1, 1)),
                ((1, -1), (1, 0), (1, 1)),
                ((-1, -1), (0, -1), (1, -1)),
                ((-1, 1), (0, 1), (1, 1)),
            ]
        )

    def move_elves(self, rounds):
        """
        >>> board = Board(example_text)
        >>> board.move_elves(1)
        1
        >>> print(board)  # 1
        |.....#...|
        |...#...#.|
        |.#..#.#..|
        |.....#..#|
        |..#.#.##.|
        |#..#.#...|
        |#.#.#.##.|
        |.........|
        |..#..#...|
        >>> board.reset()
        >>> board.move_elves(2)
        2
        >>> print(board)  # 2
        |......#....|
        |...#.....#.|
        |..#..#.#...|
        |......#...#|
        |..#..#.#...|
        |#...#.#.#..|
        |...........|
        |.#.#.#.##..|
        |...#..#....|
        >>> board.reset()
        >>> board.move_elves(10)
        10
        >>> print(board)  # 10
        |......#.....|
        |..........#.|
        |.#.#..#.....|
        |.....#......|
        |..#.....#..#|
        |#......##...|
        |....##......|
        |.#........#.|
        |...#.#..#...|
        |............|
        |...#..#..#..|
        >>> board.blank_space
        110
        >>> board.reset()
        >>> board.move_elves(maxsize)
        20
        """

        def has_neighbors(r0, c0):
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if not (dr == dc == 0):
                        r1, c1 = r0 + dr, c0 + dc
                        if (r1, c1) in self.board:
                            return True
            return False

        def no_elves(r0, c0, move_set):
            for dr, dc in move_set:
                r1, c1 = r0 + dr, c0 + dc
                if (r1, c1) in self.board:
                    # Oh no an elf!
                    return False
            return True

        for n in range(rounds):
            proposals = defaultdict(list)
            for r, c in self.board:
                if has_neighbors(r, c):
                    for move_set in self.moves:
                        if no_elves(r, c, move_set):
                            _, (dr, dc), _ = move_set
                            r1, c1 = r + dr, c + dc
                            proposals[(r1, c1)].append((r, c))
                            break
            proposals = dict(proposals)
            someone_moved = False
            for k, v in proposals.items():
                if len(v) == 1:
                    r1, c1 = k
                    [(r, c)] = v
                    self.board.remove((r, c))
                    self.board.add((r1, c1))
                    someone_moved = True
            if not someone_moved:
                return n + 1
            self.moves.rotate(-1)

    @staticmethod
    def parse(text):
        board = set()
        text = text.strip()
        for i, line in enumerate(text.split("\n")):
            for j, c in enumerate(line):
                if c == "#":
                    board.add((i, j))
        return board

    @property
    def extent(self):
        ivals = [i for (i, j) in self.board]
        jvals = [j for (i, j) in self.board]
        return min(ivals), max(ivals) + 1, min(jvals), max(jvals) + 1

    @property
    def blank_space(self):
        i0, i1, j0, j1 = self.extent
        return (i1 - i0) * (j1 - j0) - len(self.board)

    def __str__(self):
        i0, i1, j0, j1 = self.extent
        text = ""
        for i in range(i0, i1):
            text += "|"
            for j in range(j0, j1):
                text += "#" if ((i, j) in self.board) else "."
            text += "|\n"
        return text[:-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
