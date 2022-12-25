import sys


class LowBudget2DArray:
    def __init__(self, data, ny, nx):
        assert len(data) == ny * nx
        self.data = data
        self.ny = ny
        self.nx = nx

    def __getitem__(self, ndx):
        i, j = ndx
        assert 0 <= i < self.ny
        assert 0 <= j < self.nx
        return self.data[i * self.nx + j]

    def __str__(self):
        lines = []
        for i in range(self.ny):
            lines.append(
                "".join(str(int(x)) for x in self.data[i * self.nx : (i + 1) * self.nx])
            )
        return "\n".join(lines)


DIRECTION = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def find_visibility_distance(hmap, ndx, direction):
    delta = DIRECTION[direction]
    max_ndx = [hmap.ny, hmap.ny, hmap.nx, hmap.nx][direction]

    base_height = hmap[ndx]
    for i in range(max_ndx):
        ndx = tuple(x + dx for (x, dx) in zip(ndx, delta))
        if not (0 <= ndx[0] < hmap.ny) or not (0 <= ndx[1] < hmap.nx):
            return i, True
        height = hmap[ndx]
        if height >= base_height:
            return i, False

    assert False


def find_visible(hmap, i, j):
    visible = False
    for direction in range(4):
        dist, _ = find_visibility_distance(hmap, (i, j), direction)
        match direction:
            case 0:
                visible |= dist == hmap.ny - i - 1
            case 1:
                visible |= dist == i
            case 2:
                visible |= dist == hmap.nx - j - 1
            case 3:
                visible |= dist == j
    return visible


def visible_sum(hmap):
    total = 0
    for i in range(hmap.nx):
        for j in range(hmap.ny):
            total += find_visible(hmap, i, j)
    return total


def find_scenic_score(hmap, i, j):
    score = 1
    for direction in range(4):
        dist, at_edge = find_visibility_distance(hmap, (i, j), direction)
        if not at_edge:
            dist += 1
        score *= dist
    return score


def max_scenic_score(hmap):
    maxscore = 0
    for i in range(hmap.nx):
        for j in range(hmap.ny):
            maxscore = max(find_scenic_score(hmap, i, j), maxscore)
    return maxscore


def load_map(path):
    nx = None
    heights = []
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if nx is None:
                nx = len(line)
            assert len(line) == nx
            heights.extend(int(x) for x in line)
        ny = i + 1
    return LowBudget2DArray(heights, nx, ny)


if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    heights = load_map(path)
    print(visible_sum(heights))
    print(max_scenic_score(heights))
