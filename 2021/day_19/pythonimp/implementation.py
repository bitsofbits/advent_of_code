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


def key_points(points, n=12, max_offset=1500):
    """

    max_offset is 1500 rather than 1000 (as you might expect) because the other
    beacon could be midway between two points 1000 units apart.

    >>> sensors = parse(EXAMPLE_TEXT)
    >>> keys = list(key_points(sensors[0]))

    # >>> len(keys), len(sensors[0])
    # (1, 25)
    >>> sorted(keys)[0]
    (-876, 649, 763)
    """
    for i, p1 in enumerate(points):
        cnt = 0
        for j, p2 in enumerate(points):
            if j <= i:
                continue
            deltas = tuple(abs(x) for x in sub(p2, p1))
            if all(v <= max_offset for v in deltas):
                cnt += 1
            if cnt >= n - 1:
                yield p1
                break


def sub(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 - x1, y2 - y1, z2 - z1)


def add(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 + x1, y2 + y1, z2 + z1)


def tx(p, sx, sy, sz, t):
    return (sx * p[t[0]], sy * p[t[1]], sz * p[t[2]])


def find_match(target_points, pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> n = 3
    >>> other = {k : v for (k, v) in sensors.items() if k != n}
    >>> find_match(sensors[n], other)[:-1]
    ((-500, 565, -823), (-340, -569, -846), 1, (1, 1, 1, (0, 1, 2)))
    """
    key_pts1 = list(key_points(target_points))
    for lbl2, other_points in pointsets.items():
        keypts_2 = list(key_points(other_points))
        for p1 in key_pts1:
            mpts_1 = {sub(p, p1) for p in target_points}
            for p2 in keypts_2:
                relpts_2 = {sub(p, p2) for p in other_points}
                for sx in [1, -1]:
                    for sy in [1, -1]:
                        for sz in [1, -1]:
                            for t, p in [
                                ((0, 1, 2), 1),
                                ((0, 2, 1), -1),
                                ((1, 2, 0), 1),
                                ((1, 0, 2), -1),
                                ((2, 0, 1), 1),
                                ((2, 1, 0), -1),
                            ]:
                                if sx * sy * sz != p:
                                    continue
                                mpts_2 = {tx(p, sx, sy, sz, t) for p in relpts_2}
                                if len(mpts_2 & mpts_1) >= 12:
                                    return (p1, p2, lbl2, (sx, sy, sz, t), mpts_2)


def add_one_set(target_points, pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> target = sensors[0]
    >>> other = {k : v for (k, v) in sensors.items() if k != 0}
    >>> len(other)
    4
    >>> len(target)
    25
    >>> _ = add_one_set(target, other)
    >>> len(target) # 2
    38
    >>> len(other)
    3
    """
    (p1, p2, lbl2, t, mpts_2) = find_match(target_points, pointsets)
    pointsets.pop(lbl2)
    for p in {add(p, p1) for p in mpts_2}:
        if p not in target_points:
            target_points.append(p)
    # Real location of p2 is same as p1
    # Now add the transformed location of p1 relative to the sensor
    return sub(p1, tx(p2, *t))


#   +p1    p2-p1  -p2
# b1--->p1--->p2--->

location = None


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    79
    """
    global locations
    sensors = parse(text)
    locations = [(0, 0, 0)]
    for k0 in sensors:
        targets = sensors.pop(k0)
        while sensors:
            offset = add_one_set(targets, sensors)
            locations.append(offset)
            print(len(sensors))
        else:

            return len(targets)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3621
    """

    dists = []
    for i, a in enumerate(locations):
        for j, b in enumerate(locations):
            if j >= i:
                continue
            delta = sub(a, b)
            d = sum(abs(x) for x in delta)
            dists.append(d)
    return max(dists)


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()
    doctest.testmod()
