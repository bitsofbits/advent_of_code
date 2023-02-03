from itertools import count


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    (1, 5, 4)
    (2, 2, 1)
    """
    for i, line in enumerate(text.strip().split("\n")):
        _, discnum, _, n, _, _, _, _, _, _, _, pos = line[:-1].split()
        assert discnum == f"#{i + 1}", discnum
        yield i + 1, int(n), int(pos)


# Disc #1 has 5 positions; at time=0, it is at position 4.
# Disc #2 has 2 positions; at time=0, it is at position 1.


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5
    """
    discs = list(parse(text))
    for t in count():
        for dt, n, p0 in discs:
            if (t + dt + p0) % n != 0:
                break
        else:
            return t


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    85
    """
    discs = list(parse(text))
    discs.append((len(discs) + 1, 11, 0))
    for t in count():
        for dt, n, p0 in discs:
            if (t + dt + p0) % n != 0:
                break
        else:
            return t


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
