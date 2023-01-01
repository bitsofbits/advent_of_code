from collections import Counter
from itertools import combinations


def parse(text):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    """
    scanners = {}
    for chunk in text.strip().split("\n\n"):
        lines = chunk.split("\n")
        _, _, ndxstr, _ = lines[0].split()
        ndx = int(ndxstr)
        points = []
        for line in lines[1:]:
            points.append(tuple(int(x) for x in line.split(",")))
        scanners[ndx] = points
    return scanners


def key_points(points, n=12, max_offset=2000):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> keys = list(key_points(sensors[0]))

    # >>> len(keys), len(sensors[0])
    # (1, 25)
    >>> sorted(keys)[0]
    (-876, 649, 763)
    """
    keys = set()
    for i, p1 in enumerate(points):
        cnt = 0
        for j, p2 in enumerate(points):
            if j <= i:
                continue
            deltas = [abs(x) for x in sub(p2, p1)]
            if all(v <= max_offset for v in deltas):
                cnt += 1
            if cnt >= n - 1:
                yield p1
                break
    return keys


def sub(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 - x1, y2 - y1, z2 - z1)


def add(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 + x1, y2 + y1, z2 + z1)


def tx(p1, sx, sy, sz, t):
    x1, y1, z1 = p1
    x = (sx * x1, sy * y1, sz * z1)
    return (x[t[0]], x[t[1]], x[t[2]])


def find_match(target_points, pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> n = 3
    >>> other = {k : v for (k, v) in sensors.items() if k != n}
    >>> find_match(sensors[n], other)
    ((-500, 565, -823), (-340, -569, -846), 1, (1, 1, 1, (0, 1, 2)))
    """
    for lbl2, other_points in pointsets.items():
        # keypts_2 = key_points(other_points)
        for p1 in key_points(target_points):
            mpts_1 = {sub(p, p1) for p in target_points}
            for p2 in key_points(other_points):
                relpts_2 = {sub(p, p2) for p in other_points}
                for sx in [1, -1]:
                    for sy in [1, -1]:
                        for sz in [1, -1]:
                            for t in [
                                (0, 1, 2),
                                (0, 2, 1),
                                (1, 2, 0),
                                (1, 0, 2),
                                (2, 0, 1),
                                (2, 1, 0),
                            ]:
                                mpts_2 = {tx(p, sx, sy, sz, t) for p in relpts_2}
                                if len(mpts_2 & mpts_1) >= 12:
                                    return (p1, p2, lbl2, (sx, sy, sz, t))


def add_one_set(target_points, pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> target = sensors[0]
    >>> other = {k : v for (k, v) in sensors.items() if k != 0}
    >>> len(other)
    4
    >>> len(target)
    25
    >>> add_one_set(target, other)
    >>> len(target) # 2
    38
    >>> len(other)
    3
    """
    (p1, p2, lbl2, t) = find_match(target_points, pointsets)
    source_points = pointsets.pop(lbl2)
    for p in {add(tx(sub(p, p2), *t), p1) for p in source_points}:
        if p not in target_points:
            target_points.append(p)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    79
    """
    sensors = parse(text)
    for k0 in sensors:
        targets = sensors.pop(k0)
        while sensors:
            add_one_set(targets, sensors)
            print(len(sensors))
        else:
            return len(targets)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()
    doctest.testmod()
