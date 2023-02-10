from itertools import count


def parse(text):
    """
    >>> dict(parse(EXAMPLE_TEXT))
    {0: 3, 1: 2, 4: 4, 6: 4}
    """
    for line in text.strip().split("\n"):
        a, b = (int(x) for x in line.strip().split(":"))
        yield a, b


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    24
    """
    severity = 0
    for depth, rng in parse(text):
        t = depth
        period = 2 * (rng - 1)
        severity += depth * rng * (t % period == 0)
    return severity


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    10
    """
    for delay in count():
        for depth, rng in parse(text):
            t = delay + depth
            period = 2 * (rng - 1)
            if t % period == 0:
                break
        else:
            return delay


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
