import sys


class LowBudgetArray:
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


def _find_visibility_vector(hmap, ndx, direction):
    delta = [(1, 0), (-1, 0), (0, 1), (0, -1)][direction]
    steps = [hmap.ny, hmap.ny, hmap.nx, hmap.nx][direction]

    max_height = -1
    visible = []

    for _ in range(steps):
        height = hmap[ndx]
        visible.append(height > max_height)
        max_height = max(height, max_height)
        ndx = tuple(x + dx for (x, dx) in zip(ndx, delta))
    if direction % 2:
        visible = visible[::-1]
    return visible


def find_visibility_submap(hmap, direction, start=None):
    delta = [(0, 1), (0, 1), (1, 0), (1, 0)][direction]
    steps = [hmap.nx, hmap.nx, hmap.ny, hmap.ny][direction]
    if start is None:
        start = [(0, 0), (hmap.ny - 1, 0), (0, 0), (0, hmap.nx - 1)][direction]
    visible = []
    for _ in range(steps):
        visible.append(_find_visibility_vector(hmap, start, direction))
        start = tuple(x + dx for (x, dx) in zip(start, delta))
    if direction // 2 == 1:
        visible = list(list(x) for x in zip(*visible))
    visible = sum(visible, [])
    return LowBudgetArray(visible, hmap.ny, hmap.nx)


def find_visibility_map(hmap):
    vmap = find_visibility_submap(hmap, 0)
    for i in range(1, 4):
        submap = find_visibility_submap(hmap, i)
        new_data = [x or y for (x, y) in zip(vmap.data, submap.data)]
        vmap.data = new_data
    return vmap


def find_scenic_subscore(hmap, ndx, direction):
    delta = [(1, 0), (-1, 0), (0, 1), (0, -1)][direction]
    max_ndx = [hmap.ny, hmap.ny, hmap.nx, hmap.nx][direction]

    base_height = hmap[ndx]
    for i in range(max_ndx):
        ndx = tuple(x + dx for (x, dx) in zip(ndx, delta))
        if not (0 <= ndx[0] < hmap.ny) or not (0 <= ndx[1] < hmap.nx):
            return i
        height = hmap[ndx]
        if height >= base_height:
            return i + 1

    assert False


def find_scenic_score(hmap, i, j):
    score = 1
    for direction in range(4):
        score *= find_scenic_subscore(hmap, (i, j), direction)
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
    return LowBudgetArray(heights, nx, ny)


if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    heights = load_map(path)
    visible = find_visibility_map(heights)
    print(sum(visible.data))

    print(max_scenic_score(heights))
