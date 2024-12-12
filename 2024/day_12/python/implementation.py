from collections import defaultdict
from itertools import count

def parse(text):
    """
    >>> len(parse(EXAMPLE_TEXT))
    100
    """
    farm_map = {}
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            farm_map[i, j] = x
    return farm_map


def flood_fill(x, map_):
    seen = set()
    stack = [x]
    neighbors = set()
    target = map_[x]
    while stack:
        (i, j) = x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x1 = (i + di, j + dj)
            if map_.get(x1) == target:
                stack.append(x1)
                neighbors.add((x, x1))
                neighbors.add((x1, x))
    return seen, neighbors



def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1930
    """
    farm_map = parse(text)
    seen = set()
    score = 0
    for key in farm_map:
        if key in seen:
            continue
        region, neighbors = flood_fill(key, farm_map)
        seen |= set(region)
        perimeter = 4 * len(region) - len(neighbors)
        score += len(region) * perimeter
    return score

directions = {
    '>' : (0, 1),
    'v' : (1, 0),
    '<' : (0, -1),
    '^' : (-1, 0)
}

ccw_directions = {
    'v' : (0, 1),
    '<' : (1, 0),
    '^' : (0, -1),
    '>' : (-1, 0)
}

def is_outer_edge(x, d, neighbors):
    i, j = x
    di, dj = ccw_directions[d]
    x1 = (i + di, j + dj)
    return (x, x1) not in neighbors

def count_sides(region, neighbors):
    neighbor_map = defaultdict(set)
    for a, b in neighbors:
        neighbor_map[a].add(b)
    boundaries = [x for x in region if len(neighbor_map.get(x, ())) < 4]
    seen = set()
    sides = 0
    for d in '>v<^':
        for x in boundaries:
            if (d, x) in seen:
                continue
            seen.add((d, x))
            if is_outer_edge(x, d, neighbors):
                sides += 1
                # This is an outer edge so follow both directions till it stops
                di, dj = directions[d]
                i, j = x
                while True:
                    i = i + di
                    j = j + dj
                    x1 = (i, j)
                    if x1 in region and is_outer_edge(x1, d, neighbors):
                        seen.add((d, x1))
                    else:
                        break
                i, j = x
                while True:
                    i = i - di
                    j = j - dj
                    x1 = (i, j)
                    if x1 in region and is_outer_edge(x1, d, neighbors):
                        seen.add((d, x1))
                    else:
                        break
    return sides


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1206
    """
    farm_map = parse(text)
    seen = set()
    score = 0
    for key in farm_map:
        if key in seen:
            continue
        region, neighbors = flood_fill(key, farm_map)
        seen |= set(region)
        sides = count_sides(region, neighbors)
        score += len(region) * sides
    return score

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
