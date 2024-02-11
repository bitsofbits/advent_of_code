import math
from collections import Counter, defaultdict
from functools import cache
from itertools import combinations, permutations


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


@cache
def find_bounds(nanobot):
    # Convert nanobot range to its 8 bounding planes
    # Specify each plane by `p`, its z_intercept
    nanobot_location, signal_radius = nanobot
    x0, y0, z0 = nanobot_location
    planes = []
    for x_sign in (1, -1):
        for y_sign in (1, -1):
            for z_sign in (1, -1):
                z1 = z0 + z_sign * signal_radius
                N = (x_sign, y_sign, z_sign)
                P0 = (x0, y0, z1)
                # P = (x, y, z)
                # N•P - N•P0 = 0 => N•P = N.P0 = N•(0, 0, z_intercept)
                z_intercept = z_sign * dot(N, P0)
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
            if n == target_count:
                base_indices = tuple(sorted(others))
                if base_indices in tried:
                    continue
                for indices in combinations(base_indices, target_count):
                    if indices not in tried:
                        tried.add(indices)
                        yield indices


def distance_from_bounds(bounds):
    distances = []
    for i in range(4):
        z_a = bounds[i]
        z_b = bounds[7 - i]
        if z_a * z_b <= 0:
            distances.append(0)
        elif z_a < 0:
            distances.append(max(z_a, z_b))
        else:
            distances.append(min(z_a, z_b))
    index = max(range(4), key=lambda i: abs(distances[i]))
    nominal_distance = abs(distances[index])
    # The nominal distance can be off by up to 2(?) due
    # to (something, something), so check somehow

    return nominal_distance


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    36

    49355796 is too low
    100985897 is too low :-(
    100985899 is too high! (arbitrary)

    100985898 -- Suspicion is that distance_from_bounds is not quite right,
              -- and in some cases there may be no point in the region on
              -- the intersection or maybe it's there, but not on the edge and is
              -- 1 or 2 units away
              -- fix would be to find intersection 8 corners. build a bounding box and then just compute
              -- the interior
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
            key = (len(indices), -distance_from_bounds(bounds))
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
