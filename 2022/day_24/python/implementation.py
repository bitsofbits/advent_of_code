from bisect import insort_left
from collections import defaultdict, deque

example_text = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


class Valley:
    """
    >>> v = Valley(example_text)
    >>> print(v)
    #E######
    #>>.<^<#
    #.<..<<#
    #>v.><>#
    #<^v^^>#
    ######.#

    >>> v.loc = v.end_loc
    >>> print(v)
    #.######
    #>>.<^<#
    #.<..<<#
    #>v.><>#
    #<^v^^>#
    ######E#
    """

    def __init__(self, text):
        self.board = self.parse(text)
        self.max_i = max(i for (i, _) in self.board)
        self.max_j = max(j for (_, j) in self.board)
        self.start_loc = (0, 1)
        self.end_loc = (self.max_i, self.max_j - 1)
        self.loc = self.start_loc

    def parse(self, text):
        text = text.strip()
        board = defaultdict(str)
        for i, line in enumerate(text.split("\n")):
            for j, c in enumerate(line):
                if c != ".":
                    board[i, j] = c
        return board

    def traverse(self, start, end):
        """
        >>> v = Valley(example_text)
        >>> path = v.traverse(v.start_loc, v.end_loc)
        >>> len(path)
        18
        >>> path
        'vvW^>>v<^>Wvv>>>vv'
        """
        seen = set()
        boards = {0: self.board}
        dist = sum(abs(x - y) for (x, y) in zip(start, end))
        queue = [(-dist, 0, start, "")]
        while queue:
            _, t, (i, j), path = queue.pop()
            if (i, j) == end:
                self.board = boards[t]
                return path
            if (t + 1) not in boards:
                boards[t + 1] = self.find_next_blizzards(boards[t])
            next_board = boards[t + 1]
            for mv in ">v<^W":
                i1, j1 = self.move(i, j, mv)
                if (i1, j1) not in next_board and 0 <= i1 <= self.max_i:
                    # Blizzards and walls are not allowed
                    new_state = (t + 1, i1, j1)
                    if new_state not in seen:
                        est_t = t + 1 + abs(i1 - end[0]) + abs(j1 - end[1])
                        # Use the negative of estimated time so the sort is reversed
                        # and we can use pop to retrieve the value at the beginning
                        insort_left(queue, (-est_t, t + 1, (i1, j1), path + mv))
                        seen.add(new_state)
        raise RuntimeError("coud not traverse valley")

    def simple_traverse(self):
        return self.traverse(self.start_loc, self.end_loc)

    def snack_retrieval(self):
        """
        >>> v = Valley(example_text)
        >>> path = v.snack_retrieval()
        >>> len(path)
        54
        """
        p1 = self.traverse(self.start_loc, self.end_loc)
        p2 = self.traverse(self.end_loc, self.start_loc)
        p3 = self.traverse(self.start_loc, self.end_loc)
        return p1 + p2 + p3

    def move(self, i, j, c):
        match c:
            case ">":
                j += 1
            case "v":
                i += 1
            case "<":
                j -= 1
            case "^":
                i -= 1
            case "W":
                pass
            case _:
                raise ValueError(c)
        return i, j

    def find_next_blizzards(self, board):
        next_board = {}
        for (i, j), state in board.items():
            if state == "#":
                next_board[i, j] = "#"
                continue
            for c in state:
                i1, j1 = self.move(i, j, c)
                i1 = (i1 - 1) % (self.max_i - 1) + 1
                j1 = (j1 - 1) % (self.max_j - 1) + 1
                next_board[i1, j1] = next_board.get((i1, j1), "") + c
        return next_board

    def advance_blizzards(self):
        """
        >>> v = Valley(example_text)
        >>> v.advance_blizzards()
        >>> v.loc = (1, 1)
        >>> print(v)
        #.######
        #E>3.<.#
        #<..<<.#
        #>2.22.#
        #>v..^<#
        ######.#

        >>> for i in range(5): v.advance_blizzards()
        >>> v.loc = (1, 3)
        >>> print(v)
        #.######
        #>2E<.<#
        #.2v^2<#
        #>..>2>#
        #<....>#
        ######.#
        """
        self.board = self.find_next_blizzards(self.board)

    def __str__(self):
        text = ""
        for i in range(self.max_i + 1):
            for j in range(self.max_j + 1):
                c = self.board.get((i, j), ".")
                if (i, j) == self.loc:
                    assert c == "."
                    c = "E"
                if len(c) > 1:
                    c = str(len(c))
                text += c
            text += "\n"
        return text[:-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
