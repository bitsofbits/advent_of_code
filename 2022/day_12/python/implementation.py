import array
from itertools import count


class Array2D:
    def __init__(self, data, shape):
        assert len(data) == shape[0] * shape[1]
        self.data = data
        self.shape = shape

    def is_valid(self, ndx):
        i, j = ndx
        ni, nj = self.shape
        return (0 <= i < ni) and 0 <= j < nj

    def __getitem__(self, ndx):
        assert self.is_valid(ndx), f"{ndx} is our of range for shape {self.shape}"
        i, j = ndx
        ni, nj = self.shape
        return self.data[i * nj + j]

    def __str__(self):
        lines = []
        ni, nj = self.shape
        ord_a = ord("a")
        for i in range(ni):
            lines.append(
                "".join(chr(x + ord_a) for x in self.data[i * nj : (i + 1) * nj])
            )
        return "\n".join(lines)


def adjacent(ch0, ch1):
    chmap = {"E": "z", "S": "a"}
    ch0 = chmap.get(ch0, ch0)
    ch1 = chmap.get(ch1, ch1)
    return ord(ch1) - ord(ch0) <= 1


class Map:
    """An elevation map for finding better reception

    >>> map = Map("data/example.txt")
    >>> print(map)
    aabqponm
    abcryxxl
    accszzxk
    acctuvwj
    abdefghi
    >>> map.start
    (0, 0)
    >>> map.end
    (2, 5)
    """

    def __init__(self, path):

        self.start, self.end, flat_data, shape = self.build_data(path)
        self.data = Array2D(flat_data, shape)

    def build_data(self, path):
        data = []
        start = end = None
        ord_a = ord("a")
        width = None
        with open(path) as f:
            i = 0
            for r in f:
                r = r.strip()
                if r:
                    if width is None:
                        width = len(r)
                    assert width == len(r)
                    for j, c in enumerate(r):
                        match c:
                            case "S":
                                c = "a"
                                start = (i, j)
                            case "E":
                                c = "z"
                                end = (i, j)
                            case _:
                                pass
                        data.append(ord(c) - ord_a)
                    i += 1
        shape = (len(data) // width, width)
        return start, end, data, shape

    def __str__(self):
        return str(self.data)

    def get_valid_neighbors(self, pt, reverse=False):
        """

        >>> map = Map("data/example.txt")
        >>> list(map.get_valid_neighbors(map.start))
        [(1, 0), (0, 1)]
        >>> list(map.get_valid_neighbors(map.end, reverse=True))
        [(2, 4)]
        """
        (i0, j0) = pt
        ch0 = self.data[pt]
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i1, j1 = i0 + di, j0 + dj
            if not (0 <= i1 < self.data.shape[0] and 0 <= j1 < self.data.shape[1]):
                continue
            pt1 = (i1, j1)
            ch1 = self.data[pt1]
            dc = ch1 - ch0
            if reverse:
                dc *= -1
            if dc > 1:
                continue
            yield pt1

    def sample_forward(self, start_value="start"):
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
                if start_value == "start":
                    if pt1 == self.start:
                        return pt1, nodes
                elif self.data[pt1] == start_value:
                    return pt1, nodes
                used_pts.add(pt1)
        raise ValueError(f"path to {start_value} not found")

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

    def find_shortest_path(self, start_value="start"):
        """Compute shortest path length to get from start to end

        Uses Sample algorithm https://en.wikipedia.org/wiki/Pathfinding

        If we use the default start_values, we get a shortest path from
        start to end. However, if we use `{"S", "a"}` we instead get the
        answer to part 2 since it checks all start points with those values.

        >>> map = Map("data/example.txt")
        >>> len(map.find_shortest_path())
        31
        >>> len(map.find_shortest_path(0))
        29
        """
        start_pt, nodes = self.sample_forward(start_value)
        return self.sample_back(nodes, start_pt)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
