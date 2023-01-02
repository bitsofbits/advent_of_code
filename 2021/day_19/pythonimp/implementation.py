from typing import NamedTuple


class PointSet(NamedTuple):
    points: list
    # Dists are conceptually multisets, but we implement as lists
    all_dists: list
    dists_per_point: list
    offsets: set


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
        scanners[ndx] = PointSet(points, *find_dists(points), {(0, 0, 0)})
    return scanners


def find_dists(points):
    all_dists = []
    dists_per_pt = []
    for i, p1 in enumerate(points):
        x1, y1, z1 = p1
        kdists = []
        for j, p2 in enumerate(points):
            x2, y2, z2 = p2
            d = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            if j > i:
                all_dists.append(d)
            if j != i:
                kdists.append(d)
        dists_per_pt.append(kdists)
    return all_dists, dists_per_pt


def overlaps_atleast(p1, p2, n):
    s1 = set(p1)
    s2 = set(p2)
    if len(s1) == len(p1) and len(s2) == len(p2):
        return len(s1 & s2) >= n
    if len(s1 & s2) >= n:
        return True
    if sum(1 for x in p1 if x in s2) < n:
        return False
    if sum(1 for x in p2 if x in s1) < n:
        return False
    return True


def sub(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 - x1, y2 - y1, z2 - z1)


def add(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 + x1, y2 + y1, z2 + z1)


def txfm(p, sx, sy, sz, t):
    return (sx * p[t[0]], sy * p[t[1]], sz * p[t[2]])


TRANSFORMS = []
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
                if sx * sy * sz == p:
                    TRANSFORMS.append((sx, sy, sz, t))


def find_match(pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> _ = find_match(sensors)[:-1]
    """
    # By merging smaller pairs first we reduce recomputation of dists
    keys = sorted(pointsets, key=lambda k: len(pointsets[k].all_dists))
    for i, lbl1 in enumerate(keys):
        for j, lbl2 in enumerate(keys):
            if j >= i:
                continue
            points_1, all_dists_1, dists_per_pt_1, _ = pointsets[lbl1]
            points_2, all_dists_2, dists_per_pt_2, _ = pointsets[lbl2]
            if not overlaps_atleast(all_dists_1, all_dists_2, 66):
                continue
            for p1, p1_dists in zip(points_1, dists_per_pt_1):
                mpts_1 = {sub(p, p1) for p in points_1}
                for p2, p2_dists in zip(points_2, dists_per_pt_2):
                    if not overlaps_atleast(p1_dists, p2_dists, 11):
                        continue
                    relpts_2 = {sub(p, p2) for p in points_2}
                    for tx in TRANSFORMS:
                        mpts_2 = {txfm(p, *tx) for p in relpts_2}
                        if len(mpts_2 & mpts_1) >= 12:
                            return (lbl1, p1, lbl2, p2, tx, mpts_2)
    raise ValueError()


def add_one_set(pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> target, *_ = sensors[0]
    >>> other = {k : v for (k, v) in sensors.items() if k != 0}
    >>> len(sensors)
    5
    >>> _ = add_one_set(sensors)
    >>> len(sensors)
    4
    """
    (lbl1, p1, lbl2, p2, t, mpts_2) = find_match(pointsets)
    pset1 = pointsets.pop(lbl1)
    pset2 = pointsets.pop(lbl2)
    for p in {add(p, p1) for p in mpts_2}:
        if p not in pset1.points:
            pset1.points.append(p)
    for os in pset2.offsets:
        # First get the offset relative to our anchor point in frame 2
        os = sub(os, p2)
        # Then transform the offset to get it into frame 2
        os = txfm(os, *t)
        # Then shift by our anchor point in frame 2
        os = add(p1, os)
        pset1.offsets.add(os)
    pointsets[lbl1] = PointSet(pset1.points, *find_dists(pset1.points), pset1.offsets)


offsets = None


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    79
    """
    global offsets
    sensors = parse(text)
    while len(sensors) > 1:
        add_one_set(sensors)
    _, pset = sensors.popitem()
    offsets = pset.offsets
    return len(pset.points)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3621
    """
    osets = list(enumerate(offsets))
    dists = []
    for i, a in osets:
        for j, b in osets:
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
