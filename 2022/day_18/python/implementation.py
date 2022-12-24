def load_rock(path):
    """
    >>> rock = load_rock("data/example.txt")
    >>> for pt in sorted(rock): print(pt)
    (1, 2, 2)
    (1, 2, 5)
    (2, 1, 2)
    (2, 1, 5)
    (2, 2, 1)
    (2, 2, 2)
    (2, 2, 3)
    (2, 2, 4)
    (2, 2, 6)
    (2, 3, 2)
    (2, 3, 5)
    (3, 2, 2)
    (3, 2, 5)
    """
    with open(path) as f:
        rock = set()
        for line in f:
            line = line.strip()
            if line:
                x, y, z = (int(x.strip()) for x in line.split(","))
                rock.add((x, y, z))
    return rock


def cell_nbrs(pt):
    x0, y0, z0 = pt
    for dx, dy, dz in [
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    ]:
        yield (x0 + dx, y0 + dy, z0 + dz)


def count_nbrs(pt, rock):
    """
    >>> rock = load_rock("data/example.txt")
    >>> count_nbrs((1, 2, 2), rock)
    1
    """
    return sum(x in rock for x in cell_nbrs(pt))


def find_surface_area(rock):
    """
    >>> rock = load_rock("data/example.txt")
    >>> find_surface_area(rock)
    64
    >>> rock = load_rock("data/data.txt")
    >>> find_surface_area(rock)
    3470
    """
    nbrs = sum(count_nbrs(x, rock) for x in rock)
    assert nbrs % 2 == 0
    return 6 * len(rock) - nbrs


def find_exterior_surface(rock):
    """
    >>> rock = load_rock("data/example.txt")
    >>> find_exterior_surface(rock)
    58
    >>> rock = load_rock("data/data.txt")
    >>> find_exterior_surface(rock)
    58
    """
    pt = max(rock, key=lambda x: x[2])
    an_exterior_pt = (*pt[:2], pt[2] + 1)
    max_cnt = 2
    pending = {(an_exterior_pt, max_cnt)}
    complete = set()
    while pending:
        pt0, cnt = pending.pop()
        complete.add(pt0)
        if count_nbrs(pt0, rock) > 0:
            cnt = max_cnt
        else:
            cnt -= 1
        if cnt == 0:
            continue
        for pt1 in cell_nbrs(pt0):
            if pt1 not in complete and pt1 not in rock:
                pending.add((pt1, cnt))
    return sum(count_nbrs(x, rock) for x in complete)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
