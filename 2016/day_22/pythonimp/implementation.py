from __future__ import annotations

from typing import NamedTuple


class Node(NamedTuple):
    location: tuple[int, int]
    size: int
    used: int
    available: int
    percent_used: float


# /dev/grid/node-x0-y0     94T   72T    22T   76%


def parse(text):
    """
    >>> for x in list(parse(EXAMPLE_TEXT))[:3]: print(x)
    Node(location=(0, 0), size=10, used=8, available=2, percent_used=80.0)
    Node(location=(0, 1), size=11, used=6, available=5, percent_used=54.0)
    Node(location=(0, 2), size=32, used=28, available=4, percent_used=87.0)
    """
    for line in text.strip().split("\n")[2:]:
        loc, size, used, avail, pct = line.strip().split()
        _, x, y = loc.split("-")
        assert x.startswith("x") and y.startswith("y")
        x, y = (int(v[1:]) for v in [x, y])
        loc = (x, y)
        for x in [size, used, avail]:
            assert x.endswith("T")
        assert pct.endswith("%")
        yield Node(
            loc, int(size[:-1]), int(used[:-1]), int(avail[:-1]), float(pct[:-1])
        )


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7
    """
    nodes = list(parse(text))
    n_viable = 0
    for i, a in enumerate(nodes):
        if a.used == 0:
            continue
        for j, b in enumerate(nodes):
            if i == j:
                continue
            if a.used <= b.available:
                n_viable += 1
    return n_viable


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)  # 212 is too low  add 6 because we have to go around wall
    |(.) .  G |
    | .  _  . |
    | #  .  . |
    7
    """
    nodes = {nd.location: nd for nd in parse(text)}

    max_x = max(x for (x, y) in nodes)
    max_y = max(y for (x, y) in nodes)
    dest = (0, 0)
    target = (max_x, 0)
    needed = max(nodes[dest].used, nodes[target].used)
    [carrier] = (
        k
        for (k, v) in nodes.items()
        if v.available >= needed and k not in (dest, target)
    )
    available = nodes[carrier].available

    # Find row of massive items:
    massive = [k for (k, v) in nodes.items() if v.used > available]
    # By observation, massive nodes are all in the same row
    [massive_y] = set(y for (x, y) in massive)
    # If massive nodes are above carrier we go through rightmost hole
    cnt = 0
    if massive_y < carrier[1]:
        holes = set(range(max_x + 1)) - set(x for (x, y) in massive)
        hole = max(holes)
        if hole < carrier[0]:
            # If the only hole is to the left we have to go out of our way
            cnt += 2 * (carrier[0] - hole)

    # Draw the board just to help us figure out what is going on
    for y in range(max_y + 1):
        row = ["|"]
        for x in range(max_x + 1):
            assert (x, y) in nodes
            if (x, y) == dest:
                row.append("(.)")
            elif (x, y) == target:
                row.append(" G ")
            elif (x, y) == carrier:
                row.append(" _ ")
            elif nodes[x, y].used > available:
                row.append(" # ")
            else:
                row.append(" . ")
        row.append("|")
        print("".join(row))

    # Step 1 get carrier to point to left of target
    tx = target[0]
    cx, cy = carrier
    cnt += abs(tx - cx) + abs(cy)
    tx -= 1
    # Then inchworm it back to corner
    while tx > 0:
        cnt += 5
        tx -= 1
    return cnt


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
