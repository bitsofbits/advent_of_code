from math import inf

example_text = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""


dirs = [">", "v", "<", "^"]


def reverse(d):
    return dirs[(dirs.index(d) + 2) % 4]


def cross(a, b):
    return tuple(
        a[(i + 1) % 3] * b[(i + 2) % 3] - a[(i + 2) % 3] * b[(i + 1) % 3]
        for i in range(3)
    )


def negative(a):
    return tuple(-x for x in a)


class Board:
    def __init__(self, board):
        self.board = board
        self.max_r = max(r for (r, c) in board)
        self.min_c_by_r = {}
        self.max_c_by_r = {}
        self.min_r_by_c = {}
        self.max_r_by_c = {}
        for r, c in self.board:
            self.min_c_by_r[r] = min(c, self.min_c_by_r.get(r, inf))
            self.max_c_by_r[r] = max(c, self.max_c_by_r.get(r, -inf))
            self.min_r_by_c[c] = min(r, self.min_r_by_c.get(c, inf))
            self.max_r_by_c[c] = max(r, self.max_r_by_c.get(c, -inf))
        self.max_c = max(self.max_c_by_r.values())
        max_dim = max(self.max_c, self.max_r)
        self.face_size = max_dim // 4
        assert self.max_r % self.face_size == self.max_c % self.face_size == 0
        assert len(board) / self.face_size**2 == 6
        self.loc = (1, self.min_c_by_r[1])
        self.dir = ">"
        self.board[self.loc] = self.dir
        self.store_face_info(*self.loc)

    @staticmethod
    def rotate_uvecs(u1, u2, pt, d):
        """
        >>> Board.rotate_uvecs((1, 0, 0), (0, 1, 0), (0, 0, 1), ">")
        ((0, 0, -1), (0, 1, 0), (1, 0, 0))
        >>> Board.rotate_uvecs((0, 0, 1), (1, 0, 0), (0, 1, 0), "v")
        ((0, 0, 1), (0, 1, 0), (-1, 0, 0))
        >>> Board.rotate_uvecs((0, 0, 1), (1, 0, 0), (0, -1, 0), "v")
        ((0, 0, 1), (0, 1, 0), (-1, 0, 0))
        """
        u3 = cross(u1, u2)
        match d:
            case ">":
                w = u1
                u1 = negative(u3)
            case "v":
                w = negative(u2)
                u2 = u3
            case "<":
                w = negative(u1)
                u1 = u3
            case "^":
                w = u2
                u2 = negative(u3)
            case _:
                raise ValueError(d)
        pt = cross(pt, cross(w, pt))
        return u1, u2, pt

    def store_face_info(self, r0, c0):
        """
        >>> board, path = parse_text(example_text)
        >>> for x in sorted(board.edge_map): print(x, "->", board.edge_map[x])
        (0, 2, '<') -> (1, 1, 'v')
        (0, 2, '>') -> (2, 3, '<')
        (0, 2, '^') -> (1, 0, 'v')
        (0, 2, 'v') -> (1, 2, 'v')
        (1, 0, '<') -> (2, 3, '^')
        (1, 0, '>') -> (1, 1, '>')
        (1, 0, '^') -> (0, 2, 'v')
        (1, 0, 'v') -> (2, 2, '^')
        (1, 1, '<') -> (1, 0, '<')
        (1, 1, '>') -> (1, 2, '>')
        (1, 1, '^') -> (0, 2, '>')
        (1, 1, 'v') -> (2, 2, '>')
        (1, 2, '<') -> (1, 1, '<')
        (1, 2, '>') -> (2, 3, 'v')
        (1, 2, '^') -> (0, 2, '^')
        (1, 2, 'v') -> (2, 2, 'v')
        (2, 2, '<') -> (1, 1, '^')
        (2, 2, '>') -> (2, 3, '>')
        (2, 2, '^') -> (1, 2, '^')
        (2, 2, 'v') -> (1, 0, '^')
        (2, 3, '<') -> (2, 2, '<')
        (2, 3, '>') -> (0, 2, '<')
        (2, 3, '^') -> (1, 2, '<')
        (2, 3, 'v') -> (1, 0, '>')
        """
        F = self.face_size
        # find all of the faces in map (R, C) coordinates
        faces = set()
        for r, c in self.board:
            R, C = ((x - 1) // F for x in (r, c))
            faces.add((R, C))
        # define starting face to have an XY orientation with Z pointing out of the page
        # note that this is east, north, face_center, where face center is the point in
        # the center of the face. Cube is assumed to be 2x2 centered on 0 to make the
        # math easy.
        face2uvecs = {}
        R0, C0 = ((x - 1) // F for x in (r0, c0))
        starting_face = ((R0, C0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        # walk the faces of the cube and find a set of unit vector east, north that are
        # consistent with the starting face
        stack = [starting_face]
        while stack:
            f, e1, n1, pt = stack.pop()
            face2uvecs[f] = (e1, n1, pt)
            assert f in faces
            R, C = f
            for d in dirs:
                f = self.naive_move(R, C, d)
                if f in faces and f not in face2uvecs:
                    e2, n2, pt2 = self.rotate_uvecs(e1, n1, pt, d)
                    assert sum(abs(x) for x in pt2) == 1
                    stack.append((f, e2, n2, pt2))
        assert len(face2uvecs) == 6
        cntr_map = {p: (R0, C0, n, p) for ((R0, C0), (e, n, p)) in face2uvecs.items()}
        # Build a mapping of face edges to the adjacent edge and its orientation info
        self.edge_map = edge_map = {}
        for f0 in faces:
            R0, C0 = f0
            for d in dirs:
                # get the unit vectors and position of first face
                e0, n0, p0 = face2uvecs[f0]
                # find unit vector and position of the adjacent cell if we left in `d`
                e1, n1, p1 = self.rotate_uvecs(e0, n0, p0, d)
                # find the existing cell at that position
                R2, C2, n2, p2 = cntr_map[p1]
                # spin v1, v2 until they match existing unit vectors
                for i in range(0, 4):
                    if n1 == n2:
                        break
                    n1 = cross(p2, n1)
                else:
                    raise ValueError
                # find the direction to enter the face from in this transition
                d2 = dirs[(dirs.index(d) + i) % 4]
                edge_map[R0, C0, d] = (R2, C2, d2)
        assert len(edge_map) == 24, len(edge_map)

    def __str__(self):
        text = ""
        for r in range(1, self.max_r + 1):
            text += "|"
            for c in range(1, self.max_c + 1):
                text += self.board.get((r, c), " ")
            text += "|\n"
        return text[:-1]

    def naive_move(self, r0, c0, d):
        match d:
            case ">":
                return r0, c0 + 1
            case "v":
                return r0 + 1, c0
            case "<":
                return r0, c0 - 1
            case "^":
                return r0 - 1, c0
            case _:
                raise ValueError(self.dir)

    def go_straight(self, n, cube_wrap=False):
        r0, c0 = self.loc
        d0 = d1 = self.dir
        for _ in range(n):
            r1, c1 = self.naive_move(r0, c0, d0)
            if cube_wrap:
                r1, c1, d1 = self.cube_wrap(r0, c0, d0)
            else:
                dr = self.max_r_by_c[c0] - self.min_r_by_c[c0] + 1
                r1 = self.min_r_by_c[c0] + (r1 - self.min_r_by_c[c0]) % dr
                dc = self.max_c_by_r[r0] - self.min_c_by_r[r0] + 1
                c1 = self.min_c_by_r[r0] + (c1 - self.min_c_by_r[r0]) % dc
            if self.board[r1, c1] == "#":
                break
            r0, c0, d0 = r1, c1, d1
            self.board[r0, c0] = d0
        self.loc = (r0, c0)
        self.dir = d0

    def move(self, path, cube_wrap=False):
        """
        >>> board, path = parse_text(example_text)
        >>> board.move(path)
        >>> print(board)
        |        >>v#    |
        |        .#v.    |
        |        #.v.    |
        |        ..v.    |
        |...#...v..v#    |
        |>>>v...>#.>>    |
        |..#v...#....    |
        |...>>>>v..#.    |
        |        ...#....|
        |        .....#..|
        |        .#......|
        |        ......#.|
        >>> board.password
        6032

        >>> board, path = parse_text(example_text)
        >>> board.move(path, cube_wrap=True)
        >>> print(board)
        |        >>v#    |
        |        .#v.    |
        |        #.v.    |
        |        ..v.    |
        |...#..^...v#    |
        |.>>>>>^.#.>>    |
        |.^#....#....    |
        |.^........#.    |
        |        ...#..v.|
        |        .....#v.|
        |        .#v<<<<.|
        |        ..v...#.|
        >>> board.password
        5031
        >>> board.loc, board.dir
        ((5, 7), '^')
        """
        for c in path:
            match c:
                case "R":
                    self.dir = dirs[(dirs.index(self.dir) + 1) % 4]
                    self.board[self.loc] = self.dir
                case "L":
                    self.dir = dirs[(dirs.index(self.dir) - 1) % 4]
                    self.board[self.loc] = self.dir
                case int(n):
                    self.go_straight(n, cube_wrap)
                case _:
                    raise ValueError(c)

    def cube_wrap(self, r, c, d):
        """
        >>> board, path = parse_text(example_text)
        >>> board.cube_wrap(1, 9, ">")
        (1, 10, '>')
        >>> board.cube_wrap(1, 9, "<")
        (5, 5, 'v')
        >>> board.cube_wrap(6, 12, ">")
        (9, 15, 'v')
        >>> board.cube_wrap(12, 11, "v")
        (8, 2, '^')
        """

        def inv(x):
            return F - x + 1

        F = self.face_size
        R0, C0 = ((x - 1) // F for x in (r, c))
        r1, c1 = self.naive_move(r, c, d)
        R1, C1 = ((x - 1) // F for x in (r1, c1))
        if (R0, C0) == (R1, C1):
            return r1, c1, d
        dr1 = r1 - R1 * F
        dc1 = c1 - C1 * F
        R2, C2, d2 = self.edge_map[R0, C0, d]
        i = (dirs.index(d2) - dirs.index(d)) % 4
        match i:
            case 0:
                dr2 = dr1
                dc2 = dc1
            case 1:
                dr2 = dc1
                dc2 = inv(dr1)
            case 2:
                dr2 = inv(dr1)
                dc2 = inv(dc1)
            case 3:
                dr2 = inv(dc1)
                dc2 = dr1
        return dr2 + R2 * F, dc2 + C2 * F, d2

    @property
    def password(self):
        r, c = self.loc
        return 1000 * r + 4 * c + dirs.index(self.dir)


def parse_text(text):
    """
    >>> board, path = parse_text(example_text)
    >>> print(board)
    |        >..#    |
    |        .#..    |
    |        #...    |
    |        ....    |
    |...#.......#    |
    |........#...    |
    |..#....#....    |
    |..........#.    |
    |        ...#....|
    |        .....#..|
    |        .#......|
    |        ......#.|
    >>> path
    [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]
    """
    text = text.strip("\n")
    board_text, path_text = text.split("\n\n")
    # turn map into a hash, could use a 2D array, but
    # the wrapping makes it not super array friendly anyway
    board = {}
    for i, line in enumerate(board_text.split("\n")):
        for j, c in enumerate(line):
            if c != " ":
                # Board is numbered from (1, 1) in the upper left
                board[i + 1, j + 1] = c
    path_text = path_text.strip()
    path = []
    while path_text:
        number_text = ""
        while path_text and path_text[0] in "0123456789":
            number_text += path_text[0]
            path_text = path_text[1:]
        if number_text:
            path.append(int(number_text))
        if path_text:
            path.append(path_text[0])
            path_text = path_text[1:]

    return Board(board), path


if __name__ == "__main__":
    import doctest

    doctest.testmod()
