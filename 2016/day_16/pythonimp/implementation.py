def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0]
    """
    return [int(x) for x in text.strip()]


def step(a):
    """
    >>> step([1])
    [1, 0, 0]
    >>> step([0])
    [0, 0, 1]
    >>> step(parse("111100001010"))
    [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    """
    n = len(a)
    a.append(0)
    a.extend(1 - x for x in a[n - 1 :: -1])
    return a


def checksum(x):
    while len(x) % 2 == 0:
        x = [(a == b) for (a, b) in zip(x[0::2], x[1::2])]
    return [int(v) for v in x]


def process(seed, length):
    """
    >>> process(parse("10000"), 20)
    [0, 1, 1, 0, 0]
    """
    fill = seed
    while len(fill) < length:
        fill = step(fill)
    fill = fill[:length]
    return checksum(fill)


def part_1(text):
    return "".join(str(x) for x in process(parse(text), 272))


def part_2(text):
    return "".join(str(x) for x in process(parse(text), 35651584))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
