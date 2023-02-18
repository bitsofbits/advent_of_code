from collections import defaultdict
from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [0, 3, 6]
    """
    return [int(x) for x in text.strip().split(",")]


def part_1(text, n=2020):
    """
    >>> part_1(EXAMPLE_TEXT)
    436
    >>> part_1("3,2,1")
    438
    """
    last = {}
    start = parse(text)
    for i, x in enumerate(start):
        next_x = i - last.get(x, i)
        last[x] = i
    for i in range(len(start), n):
        x = next_x
        next_x = i - last.get(x, i)
        last[x] = i
    return x


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    175594
    """
    return part_1(text, 30_000_000)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
