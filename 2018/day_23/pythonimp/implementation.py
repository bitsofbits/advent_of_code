import math
from collections import Counter, defaultdict
from functools import cache
from itertools import combinations, permutations
from math import inf

import numpy as np


def sign(x):
    return int(x > 0) - int(x < 0)


def parse_line(x):
    a, b = x.strip().rsplit(', ', 1)
    _, xyz = a.split('=')
    pos = tuple(int(x) for x in xyz[1:-1].split(','))
    _, radius = b.split('=')
    return pos, int(radius)


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[1]
    ((1, 0, 0), 1)
    """
    return [parse_line(x) for x in text.strip().split('\n')]


def distance(A, B):
    return sum(abs(a - b) for (a, b) in zip(A, B))


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7
    """
    nanobots = parse(text)
    origin, max_distance = max(nanobots, key=lambda x: x[-1])
    return sum(distance(location, origin) <= max_distance for (location, _) in nanobots)


# def bounds(center, radius):
#     return [(x - radius, x + radius) for x in center]


@cache
def intersect(points, nanobot):
    nanobot_location, signal_radius = nanobot
    intersection = set()
    for point in points:
        if distance(point, nanobot_location) <= signal_radius:
            intersection.add(point)
    return frozenset(intersection)


def dot(A, B):
    return sum(a * b for (a, b) in zip(A, B))


def normal_from_index(i):
    x = [1, -1][(i & 4) > 0]
    y = [1, -1][(i & 2) > 0]
    z = [1, -1][(i & 1) > 0]
    return (x, y, z)


@cache
def find_bounds(nanobot):
    # Convert nanobot range to its 8 bounding planes
    # Specify each plane by `p`, its z_intercept
    P0, radius = nanobot
    x0, y0, z0 = P0
    planes = []
    for i in range(8):
        N = normal_from_index(i)
        Nz = N[-1]
        z1 = z0 + Nz * radius
        P0 = (x0, y0, z1)
        # P = (x, y, z)
        # N•P - N•P0 = 0 => N•P = N.P0 = N•(0, 0, z_intercept)
        # Nz (N•P0) = Nz*Nz*z_intercept = z_intercept
        z_intercept = Nz * dot(N, P0)
        planes.append(z_intercept)
    return planes


def find_candidates(pairwise):
    counts = Counter(sorted(len(x) for x in pairwise)).most_common()
    counts.sort(reverse=True)

    available = 0
    for neighbors, n in counts:
        available += n
        if available >= neighbors:
            min_count = neighbors
            break

    tried = set()
    for target_count in reversed(range(1, min_count + 1)):
        for others in pairwise:
            n = len(others)
            if n == target_count <= n <= min_count:
                base_indices = tuple(sorted(others))
                for indices in combinations(base_indices, target_count):
                    if indices not in tried:
                        tried.add(indices)
                        yield indices


def find_a_corner(bounds, axis=0, end=0, which=0):
    assert 0 <= axis < 3
    assert end in (0, 1)
    values = [[0, 1], [0, 2], [0, 4]]
    values[axis] = [values[axis][end]]
    indices = []
    for a in values[0]:
        for b in values[1]:
            for c in values[2]:
                indices.append(a + b + c)
    i0, i1, i2 = (indices[(i + which) % 4] for i in range(3))
    n0, n1, n2 = (normal_from_index(i) for i in (i0, i1, i2))
    A = np.stack([n0, n1, n2], axis=0)
    V = np.array([bounds[i] * A[j, 2] for (j, i) in enumerate((i0, i1, i2))])
    return tuple(np.linalg.solve(A, V))


def is_inside(bounds, P):
    for i in range(8):
        N = normal_from_index(i)
        Nz = N[-1]
        # N•P = Nz B_i on plane
        # N•P - Nz B_i > 0 outside of plane
        if dot(N, P) > Nz * bounds[i]:
            # print(dot(N, P), Nz * bounds[i] > 0, bounds)
            return False
    return True


def distance_from_bounds(bounds):
    # There is a clever way to compute distances that isn't quite
    # right since the shapes are weird. So just build a bounding box
    # from all the corners and check what is inside

    mins = [inf] * 3
    maxs = [-inf] * 3
    for axis in range(3):
        for end in (0, 1):
            for which in range(4):
                corner = find_a_corner(bounds, axis, end, which)
                mins = [min(a, b) for (a, b) in zip(corner, mins)]
                maxs = [max(a, b) for (a, b) in zip(corner, mins)]

    valid_distances = set()
    for x in range(math.floor(mins[0]), math.ceil(maxs[0] + 1)):
        for y in range(math.floor(mins[1]), math.ceil(maxs[1] + 1)):
            for z in range(math.floor(mins[2]), math.ceil(maxs[2] + 1)):
                P = (x, y, z)
                if is_inside(bounds, P):
                    valid_distances.add(sum(abs(v) for v in P))
    if not valid_distances:
        return None
    return min(valid_distances)


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    36

    100985898
    """
    nanobots = parse(text)

    # for x in nanobots:
    #     print(x)
    #     print(find_bounds(x))

    @cache
    def intersection(indices):
        if len(indices) == 1:
            return find_bounds(nanobots[indices[0]])
        n = len(indices) // 2
        bounds_a = intersection(indices[:n])
        if bounds_a is None:
            return None
        bounds_b = intersection(indices[n:])
        if bounds_b is None:
            return None
        merged = []
        for i, (a, b) in enumerate(zip(bounds_a, bounds_b, strict=True)):
            if i % 2:
                merged.append(max(a, b))
            else:
                merged.append(min(a, b))
        merged = tuple(merged)
        # merged = tuple(min(a, b) for (a, b) in zip(bounds_a, bounds_b, strict=True))
        for i in (0, 2, 4, 6):
            # z_hat positive iterate over faces with positive z_hat
            # If matching p[i] < p[7-1] then the order of the faces is flipped and
            # there is no intersection
            if merged[i] < merged[7 - i]:
                return None
        return merged

    base_indices = list(range(len(nanobots)))

    # Find all pairwise intersections
    pairwise = [[i] for i in base_indices]
    for i in base_indices:
        for j in base_indices[i + 1 :]:
            bounds = intersection((i, j))
            if bounds is not None:
                pairwise[i].append(j)
                pairwise[j].append(i)

    best = None
    for indices in find_candidates(pairwise):
        if best and len(indices) < best[0]:
            break
        bounds = intersection(indices)
        if bounds is not None:
            distance = distance_from_bounds(bounds)
            # print(len(indices), distance, bounds)
            if distance is not None:
                key = (len(indices), -distance)
                if best is None:
                    best = key
                best = max(key, best)
    return -best[1]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
