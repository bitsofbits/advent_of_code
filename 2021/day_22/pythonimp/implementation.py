def parse_loc(text, which):
    w, rng = text.split("=")
    assert w == which, (w, which)
    return tuple(int(v) for v in rng.split(".."))


def parse_line(line):
    """
    >>> parse_line("on x=-20..26,y=-36..17,z=-47..7")
    (1, (-20, 26), (-36, 17), (-47, 7))
    >>> parse_line("off x=-48..-32,y=26..41,z=-47..-37")
    (0, (-48, -32), (26, 41), (-47, -37))
    """
    state, location = line.strip().split()
    state = {"off": 0, "on": 1}[state]
    xloc, yloc, zloc = location.split(",")
    locs = (parse_loc(xloc, "x"), parse_loc(yloc, "y"), parse_loc(zloc, "z"))
    return (state, *locs)


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT)[:4]: print(x)
    (1, (-20, 26), (-36, 17), (-47, 7))
    (1, (-20, 33), (-21, 23), (-26, 28))
    (1, (-22, 28), (-29, 23), (-38, 16))
    (1, (-46, 7), (-6, 46), (-50, -1))
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


def reboot(steps, clip_to_init_region):
    interactions = []
    for i, (sb, (bx1, bx2), (by1, by2), (bz1, bz2)) in enumerate(steps):
        if clip_to_init_region:
            region = (bx1, bx2), (by1, by2), (bz1, bz2)
            if (region := clip_region(region, [(-50, 50)] * 3)) is None:
                continue
            (bx1, bx2), (by1, by2), (bz1, bz2) = region

        pending = []
        for sa, (ax1, ax2), (ay1, ay2), (az1, az2) in interactions:
            if (
                ax2 >= bx1
                and ax1 <= bx2
                and ay2 >= by1
                and ay1 <= by2
                and az2 >= bz1
                and az1 <= bz2
            ):
                pending.append(
                    (
                        -sa,
                        # Intersection
                        (max(ax1, bx1), min(ax2, bx2)),
                        (max(ay1, by1), min(ay2, by2)),
                        (max(az1, bz1), min(az2, bz2)),
                    )
                )
        for x in pending:
            interactions.append(x)
        if sb:
            interactions.append((sb, (bx1, bx2), (by1, by2), (bz1, bz2)))

    return sum(s * volume(r) for (s, *r) in interactions)


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
