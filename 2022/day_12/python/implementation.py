import math
from itertools import count


def adjacent(ch0, ch1):
    chmap = {"E": "z", "S": "a"}
    ch0 = chmap.get(ch0, ch0)
    ch1 = chmap.get(ch1, ch1)
    return ord(ch1) - ord(ch0) <= 1


class Map:
    """An elevation map for finding better reception

    >>> map = Map("data/example.txt")
    >>> print(map)
    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
    >>> map.start
    (0, 0)
    >>> map.end
    (2, 5)
    """

    def __init__(self, path):
        rows = []
        width = None
        with open(path) as f:
            for r in f:
                r = r.strip()
                if r:
                    if width is None:
                        width = len(r)
                    assert width == len(r)
                    rows.append(r)
        self.shape = (len(rows), width)
        self.rows = rows
        self.start = self.find_char_loc("S")
        self.end = self.find_char_loc("E")

    def __str__(self):
        return "\n".join(self.rows)

    def find_char_loc(self, x):
        locs = set()
        for i, row in enumerate(self.rows):
            for j, char in enumerate(row):
                if char == x:
                    locs.add((i, j))
        [loc] = locs
        return loc

    def get_valid_neighbors(self, pt, reverse=False):
        """

        >>> map = Map("data/example.txt")
        >>> list(map.get_valid_neighbors(map.start))
        [(1, 0), (0, 1)]
        >>> list(map.get_valid_neighbors(map.end, reverse=True))
        [(2, 4)]
        """
        (i0, j0) = pt
        ch0 = self.rows[i0][j0]
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i1, j1 = i0 + di, j0 + dj
            if not (0 <= i1 < self.shape[0] and 0 <= j1 < self.shape[1]):
                continue
            ch1 = self.rows[i1][j1]
            if reverse:
                if not adjacent(ch1, ch0):
                    continue
            else:
                if not adjacent(ch0, ch1):
                    continue
            yield (i1, j1)

    def sample_forward(self):
        nodes = [(self.end, 0)]
        used_pts = set(pt for (pt, _) in nodes)
        for i in count():
            if i >= len(nodes):
                break
            pt0, counter = nodes[i]
            for pt1 in self.get_valid_neighbors(pt0, reverse=True):
                if pt1 in used_pts:
                    continue
                nodes.append((pt1, counter + 1))
                used_pts.add(pt1)
        return nodes

    def sample_back(self, nodes, start):
        by_pt = dict(nodes)
        pt = start
        path = []
        while True:
            candidates = [
                x for x in self.get_valid_neighbors(pt, reverse=False) if x in by_pt
            ]
            candidates.sort(key=lambda x: by_pt[x])
            if not candidates:
                break
            pt = candidates[0]
            path.append(pt)
            if pt == self.end:
                break
        return path

    def find_shortest_path(self, start_values=("S",)):
        """Compute shortest path length to get from start to end

        Uses Sample algorithm https://en.wikipedia.org/wiki/Pathfinding

        We break this into two parts so that we can speed up part 2 of the
        problem by only computing the map once.

        If we use the default start_values, we get a shortest path from
        start to end. However, if we use `{"S", "a"}` we instead get the
        answer to part 2 since it checks all start points with those values.

        >>> map = Map("data/example.txt")
        >>> len(map.find_traverse())
        31
        """
        start_values = set(start_values)
        nodes = self.sample_forward()
        min_steps = math.inf
        min_path = None
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.rows[i][j] in start_values:
                    path = self.sample_back(nodes, (i, j))
                    if not path or path[-1] != self.end:
                        continue
                    if len(path) < min_steps:
                        min_steps = len(path)
                        min_path = path
        return min_path


if __name__ == "__main__":
    import doctest

    doctest.testmod()
