from collections import defaultdict
from functools import cache
from itertools import count


@cache
def to_xy(n):
    if n == 1:
        return (0, 0)
    ring = 1
    edge = 2
    start = 2
    while True:
        next_start = start + 4 * edge
        if next_start > n:
            break
        start = next_start
        edge += 2
        ring += 1
    delta = (n - start + 1) % (4 * edge)
    if delta < edge:
        return ring, delta - ring
    elif delta < 2 * edge:
        return -(delta - (edge + ring)), ring
    elif delta < 3 * edge:
        return -ring, -(delta - (2 * edge + ring))
    else:
        return (delta - (3 * edge + ring)), -ring


def part_1(text):
    """
    >>> part_1("1")
    0
    >>> part_1("12")
    3
    >>> part_1("23")
    2
    >>> part_1("1024")
    31
    >>> part_1(EXAMPLE_TEXT)
    438
    """
    n = int(text)
    x, y = to_xy(n)
    return abs(x) + abs(y)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    266330
    """
    target = int(text)
    values = defaultdict(int)
    values[0, 0] = 1
    for n in count(2):
        x0, y0 = to_xy(n)
        v = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                v += values[x0 + dx, y0 + dy]
        if v > target:
            return v
        assert values[x0, y0] == 0
        values[x0, y0] = v


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
