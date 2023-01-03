from bisect import bisect_left, bisect_right


def parse_loc(text, which):
    w, rng = text.split("=")
    assert w == which, (w, which)
    return tuple(int(v) for v in rng.split(".."))


def parse_line(line):
    """
    >>> parse_line("on x=-20..26,y=-36..17,z=-47..7")
    (1, ((-20, 26), (-36, 17), (-47, 7)))
    >>> parse_line("off x=-48..-32,y=26..41,z=-47..-37")
    (0, ((-48, -32), (26, 41), (-47, -37)))
    """
    state, location = line.strip().split()
    state = {"off": 0, "on": 1}[state]
    xloc, yloc, zloc = location.split(",")
    locs = (parse_loc(xloc, "x"), parse_loc(yloc, "y"), parse_loc(zloc, "z"))
    return state, locs


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT)[:4]: print(x)
    (1, ((-20, 26), (-36, 17), (-47, 7)))
    (1, ((-20, 33), (-21, 23), (-26, 28)))
    (1, ((-22, 28), (-29, 23), (-38, 16)))
    (1, ((-46, 7), (-6, 46), (-50, -1)))
    """
    return [parse_line(line) for line in text.strip().split("\n")]


def clip(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x


def clip_rng(rng, a, b):
    x, y = rng
    return (clip(x, a, b), clip(y, a, b))


def is_empty(rng):
    x, y = rng
    return x >= y


def intersects(rgn_a, rgn_b):
    ((ax1, ax2), (ay1, ay2), (az1, az2)) = rgn_a
    ((bx1, bx2), (by1, by2), (bz1, bz2)) = rgn_b
    return (
        (ax2 >= bx1 and ax1 <= bx2)
        and (ay2 >= by1 and ay1 <= by2)
        and (az2 >= bz1 and az1 <= bz2)
    )


def lin_contained_in(rng_a, rng_b):
    a1, a2 = rng_a
    b1, b2 = rng_b
    return a1 <= b1 <= a2 and a1 <= b2 <= a2


def contained_in(rgn_a, rgn_b):
    (ax, ay, az) = rgn_a
    (bx, by, bz) = rgn_b
    return (
        lin_contained_in(ax, bx)
        and lin_contained_in(ay, by)
        and lin_contained_in(az, bz)
    )


def lin_intersection(rng_a, rng_b):
    """
    ---- ----  -> None

    -----
       -----   ->  (b1, a2)

    -----
     ---       ->  (b1, b2)

     ---
    -----      ->  (a1, a2)
    """
    a1, a2 = rng_a
    b1, b2 = rng_b
    x1 = max(a1, b1)
    x2 = min(a2, b2)
    if x1 > x2:
        return None
    return x1, x2


def intersection(rgn_a, rgn_b):
    (ax, ay, az) = rgn_a
    (bx, by, bz) = rgn_b
    if (ix := lin_intersection(ax, bx)) is None:
        return None
    if (iy := lin_intersection(ay, by)) is None:
        return None
    if (iz := lin_intersection(az, bz)) is None:
        return None
    return (ix, iy, iz)


def compute_interaction(step_a, step_b):
    """Affect of step_b coming after step_a"""
    sa, region_a = step_a
    sb, region_b = step_b
    if intersects(region_a, region_b):
        return [(-sa, intersection(region_a, region_b))]
    else:
        return []


def volume(ranges):
    (x0, x1), (y0, y1), (z0, z1) = ranges
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def clip_region(region, cube):
    assert len(region) == len(cube)
    ranges = []
    for rng, interval in zip(region, cube):
        if is_empty(rng := clip_rng(rng, *interval)):
            return None
        ranges.append(rng)
    return tuple(ranges)


def sort_x0(x):
    return x[1][0][0]


def reboot(steps, clip_to_init_region):
    interactions = []
    for i, step_b in enumerate(steps):
        if clip_to_init_region:
            s, region = step_b
            if (region := clip_region(region, [(-50, 50)] * 3)) is None:
                continue
            step_b = (s, region)
        for i in range(len(interactions)):
            current = interactions[i]
            interactions.extend(compute_interaction(current, step_b))
        if step_b[0]:
            interactions.append(step_b)
    for x in interactions:
        assert x[0] in (1, -1)
    return sum(s * volume(r) for (s, r) in interactions)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    590784

    >>> part_1(EXAMPLE2_TEXT)
    474140
    """
    global total

    steps = parse(text)
    return reboot(steps, clip_to_init_region=True)


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    2758514936282235


    1133805115975417 too low
    """
    steps = parse(text)
    return reboot(steps, clip_to_init_region=False)


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open("../data/example2.txt") as f:
        EXAMPLE2_TEXT = f.read()

    doctest.testmod()
