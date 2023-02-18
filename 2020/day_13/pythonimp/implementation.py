import math
from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    (939, [7, 13, None, None, 59, None, 31, 19])
    """
    depart, buses = text.strip().split()
    buses = [None if (x == "x") else int(x) for x in buses.split(",")]
    return int(depart), buses


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    295
    """
    depart, buses = parse(text)
    # want min(N * b - depart) => min(b - depart % b)
    wait, bus = min((b - depart % b, b) for b in buses if b is not None)
    return wait * bus


EXAMPLE_TEXT_5 = """
0
67,7,x,59,61
"""

EXAMPLE_TEXT_6 = """
0
1789,37,47,1889
"""


def merge(t0, b0, t1, b1):
    "Return a repeating period b, and offset i, than combines the two timetables"
    for t in count(t0, b0):
        if t % b1 == t1:
            b = b0 * b1
            return b - (-t) % b, b


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1068781
    >>> part_2(EXAMPLE_TEXT_5)
    1261476
    >>> part_2(EXAMPLE_TEXT_6)
    1202161486
    """
    _, buses = parse(text)
    # Compute the individual solutions and there period for each case
    solutions = [((-i) % b, b) for (i, b) in enumerate(buses) if b is not None]
    # requirements.sort(reverse=True)

    # Make sure all bus periods are prime, if they aren't there
    # are other simplifications we should try
    for _, b in solutions:
        for x in range(2, int(math.sqrt(b))):
            assert b % x != 0

    # Recursively merge the solutions
    t0, b0 = solutions[0]
    for t1, b1 in solutions[1:]:
        t0, b0 = merge(t0, b0, t1, b1)
    return t0


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
