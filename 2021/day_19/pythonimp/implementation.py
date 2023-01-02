from collections import defaultdict
from functools import cache


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
        scanners[ndx] = (points, find_dists(points), {(0, 0, 0)})
    return scanners


# def key_points(points, n=12, max_offset=1500):
#     """

#     max_offset is 1500 rather than 1000 (as you might expect) because the other
#     beacon could be midway between two points 1000 units apart.

#     >>> sensors = parse(EXAMPLE_TEXT)
#     >>> keys = list(key_points(sensors[0][0]))

#     # >>> len(keys), len(sensors[0])
#     # (1, 25)
#     >>> sorted(keys)[0]
#     (-876, 649, 763)
#     """
#     for i, p1 in enumerate(points):
#         cnt = 0
#         for j, p2 in enumerate(points):
#             if j <= i:
#                 continue
#             deltas = tuple(abs(x) for x in sub(p2, p1))
#             if all(v <= max_offset for v in deltas):
#                 cnt += 1
#             if cnt >= n - 1:
#                 yield p1
#                 break


def find_dists(points, max_offset=1500, n=12):
    dists = []
    key_points = []
    cache
    for i, p1 in enumerate(points):
        x1, y1, z1 = p1
        kdists = []
        for j, p2 in enumerate(points):
            x2, y2, z2 = p2
            d = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
            if j > i:
                dists.append(d)
            kdists.append(d)
        key_points.append((p1, kdists))

    return dists, key_points


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
        return True
    return False


def sub(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 - x1, y2 - y1, z2 - z1)


def add(p2, p1):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x2 + x1, y2 + y1, z2 + z1)


def neg(p):
    x1, y1, z1 = p
    return (-x1, -y1, -z1)


@cache
def tx(p, sx, sy, sz, t):
    return (sx * p[t[0]], sy * p[t[1]], sz * p[t[2]])


def find_match(pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> _ = find_match(sensors)[:-1]

    # (1, (686, 422, 578), (-618, -824, -621), 0, (-1, 1, -1, (0, 1, 2)))
    """
    for lbl1, (points_1, (dists_1, keypts_1), offsets) in pointsets.items():
        for lbl2, (points_2, (dists_2, keypts_2), offsets) in pointsets.items():
            if lbl1 >= lbl2:
                continue
            if len(pointsets) > 2 and not overlaps_atleast(dists_1, dists_2, 66):
                continue
            for p1, kdists1 in keypts_1:
                mpts_1 = {sub(p, p1) for p in points_1}
                for p2, kdists2 in keypts_2:
                    if not overlaps_atleast(kdists1, kdists2, 11):
                        continue
                    relpts_2 = {sub(p, p2) for p in points_2}
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
                                        return (
                                            lbl1,
                                            p1,
                                            p2,
                                            lbl2,
                                            (sx, sy, sz, t),
                                            mpts_2,
                                        )
    raise ValueError()


def add_one_set(pointsets):
    """
    >>> sensors = parse(EXAMPLE_TEXT)
    >>> target, _, _ = sensors[0]
    >>> other = {k : v for (k, v) in sensors.items() if k != 0}
    >>> len(sensors)
    5
    >>> _ = add_one_set(sensors)
    >>> len(sensors)
    4
    """
    (lbl1, p1, p2, lbl2, t, mpts_2) = find_match(pointsets)
    _, _, offsets2 = pointsets.pop(lbl2)
    target_points, _, offsets = pointsets.pop(lbl1)
    for p in {add(p, p1) for p in mpts_2}:
        if p not in target_points:
            target_points.append(p)
    offsets.update(add(p1, tx(sub(o, p2), *t)) for o in offsets2)
    pointsets[lbl1] = (target_points, find_dists(target_points), offsets)
    # Real location of p2 is same as p1
    # Now add the transformed location of p1 relative to the sensor
    # return ((lbl1, lbl2), sub(p1, tx(p2, *t)))


#   +p1    p2-p1  -p2
# b1--->p1--->p2--->

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
        print(len(sensors))
    _, (targets, _, offsets) = sensors.popitem()
    return len(targets)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3621
    """
    # sensors = parse(text)
    # lbl = list(sensors)[0]
    # locations = {lbl: (0, 0, 0)}
    # omap = defaultdict(set)
    # for ((l1, l2), v) in offsets:
    #     omap[l1].add((l2, v))
    #     omap[l2].add((l1, neg(v)))

    # stack = [lbl]
    # while stack:
    #     lbl = stack.pop()
    #     for l2, delta in omap[lbl]:
    #         loc = locations[lbl]
    #         if l2 not in locations:
    #             locations[l2] = sub(loc, delta)
    #             stack.append(l2)

    # print(offsets)
    # print(locations)
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
