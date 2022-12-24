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

    def traverse(self, start, end, initial_advance=True):
        """
        >>> v = Valley(example_text)
        >>> path = v.traverse(v.start_loc, v.end_loc)
        >>> len(path)
        18
        >>> path
        'vvW^>>v<^>Wvv>>>vv'
        """

        state = (0, start, "")
        seen = set()
        queue = deque([state])
        t0 = -1 if initial_advance else 0
        while queue:
            t, (i, j), path = queue.popleft()
            if t > t0:
                self.advance_blizzards()
                t0 = t
            if (i, j) == end:
                return path

            for mv in ">v<^W":
                i1, j1 = self.move(i, j, mv)
                if i1 >= 0 and (i1, j1) not in self.board:
                    # Blizzards and walls are not allowed
                    if (t + 1, i1, j1) not in seen:
                        queue.append((t + 1, (i1, j1), path + mv))
                        seen.add((t + 1, i1, j1))
        raise RuntimeError("cloud not traverse valley")

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
        p2 = self.traverse(self.end_loc, self.start_loc, initial_advance=False)
        p3 = self.traverse(self.start_loc, self.end_loc, initial_advance=False)
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
        next_board = {}
        for (i, j), state in self.board.items():
            if state == "#":
                next_board[i, j] = "#"
                continue
            for c in state:
                i1, j1 = self.move(i, j, c)
                i1 = (i1 - 1) % (self.max_i - 1) + 1
                j1 = (j1 - 1) % (self.max_j - 1) + 1
                next_board[i1, j1] = next_board.get((i1, j1), "") + c
        self.board = next_board

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
