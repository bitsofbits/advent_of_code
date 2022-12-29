from collections import deque
from math import inf

EXAMPLE_TEXT = """
199
200
208
210
200
207
240
269
260
263
"""


def parse(text):
    for line in text.strip().split("\n"):
        yield int(line.strip())


def window_sum(values, n):
    accum = deque(maxlen=n)
    for x in values:
        accum.append(x)
        if len(accum) == n:
            yield sum(accum)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7
    """
    last = inf
    count = 0
    for value in parse(text):
        if value > last:
            count += 1
        last = value
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    5
    """
    last = inf
    count = 0
    for value in window_sum(parse(text), 3):
        if value > last:
            count += 1
        last = value
    return count


if __name__ == "__main__":
    import doctest

    doctest.testmod()
