from itertools import cycle


def load_rocks(path):
    """
    >>> for x in load_rocks("data/rocks.txt"): print(sorted(x))
    [(0, 0), (1, 0), (2, 0), (3, 0)]
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    [(0, 0), (0, 1), (0, 2), (0, 3)]
    [(0, 0), (0, 1), (1, 0), (1, 1)]
    """
    with open(path) as f:
        text = f.read().strip()
    rocks = []
    for block in text.split("\n\n"):
        lines = block.strip().split("\n")
        n = len(lines) - 1
        pts = set()
        for i, line in enumerate(lines):
            for j, c in enumerate(line.strip()):
                if c == "#":
                    pts.add((j, n - i))
        rocks.append(pts)
    return rocks


def load_winds(path):
    """
    >>> winds = load_winds("data/example.txt")
    >>> winds[:10]
    [1, 1, 1, -1, -1, 1, -1, 1, 1, -1]
    """
    winds = []
    lookup = {"<": -1, ">": 1}
    with open(path) as f:
        for c in f.read().strip():
            winds.append(lookup[c])
    return winds


class Cave:
    """
    >>> rocks = load_rocks("data/rocks.txt")
    >>> winds = load_winds("data/example.txt")
    >>> _ = cave = Cave(rocks, winds)
    >>> cave.run(2)
    >>> print(cave.render(4))
    |...#...|
    |..###..|
    |...#...|
    |..####.|
    +-------+
    >>> cave = Cave(rocks, winds)
    >>> _ = cave.run(2022)
    >>> cave.height
    3068
    >>> cave.compute_height(1000000000000)
    1514285714288
    >>> winds = load_winds("data/data.txt")
    >>> cave = Cave(rocks, winds)
    >>> _ = cave.run(2022)
    >>> cave.height
    3181
    >>> cave.compute_height(1000000000000)
    1570434782634
    """

    width = 7

    def __init__(self, rocks, winds):
        self.rocks = rocks
        self.winds = winds
        self.stack = set()

    def render(self, height):
        lines = ["+" + "-" * self.width + "+"]
        for i in range(1, height + 1):
            row = "|"
            for j in range(1, self.width + 1):
                row += "#" if (j, i) in self.stack else "."
            row += "|"
            lines.append(row)
        return "\n".join(lines[::-1])

    @property
    def height(self):
        return max(y for (x, y) in self.stack)

    def is_valid(self, rock):
        if rock & self.stack:
            return False
        for x, y in rock:
            if x <= 0 or x > 7:
                return False
            if y <= 0:
                return False
        return True

    def _run(self):
        self.stack.clear()
        x0, y0 = 3, 4
        winds = iter(enumerate(cycle(self.winds)))
        rocks = iter(enumerate(cycle(self.rocks)))
        rock_i, raw_rock = next(rocks)
        rock = {(x0 + x, y0 + y) for (x, y) in raw_rock}
        while True:
            wind_i, dx = next(winds)
            candidate = {(x + dx, y) for (x, y) in rock}
            if self.is_valid(candidate):
                rock = candidate
            candidate = {(x, y - 1) for (x, y) in rock}
            if self.is_valid(candidate):
                rock = candidate
            else:
                self.stack |= rock
                yield rock_i % len(self.rocks), wind_i % len(self.winds)
                y0 = max(y for (x, y) in self.stack) + 4
                rock_i, raw_rock = next(rocks)
                rock = {(x0 + x, y0 + y) for (x, y) in raw_rock}

    def run(self, n_rocks):
        for i, _ in enumerate(self._run()):
            if i + 1 == n_rocks:
                break

    def compute_height(self, n_rocks):
        patterns = {}
        reps = 2
        for i, (rock_i, wind_i) in enumerate(self._run()):
            if i == n_rocks:
                return self.height

            key = (rock_i, wind_i)
            if key in patterns:
                i0, h0, cnt = patterns[key]
                if cnt >= reps:
                    break
                patterns[key] = i, self.height, cnt + 1
            else:
                patterns[key] = i, self.height, 0
        i0, h0, cnt = patterns[key]
        dn = i - i0
        dh = self.height - h0
        self.run(n_rocks % dn + dn)
        return self.height + (n_rocks - dn) // dn * dh


if __name__ == "__main__":
    import doctest

    doctest.testmod()
