from itertools import cycle


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 1, -2]
    """
    return [int(x.strip()) for x in text.split()]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    0
    """
    return sum(parse(text))


def part_2(text):
    """
    >>> part_2('+1\\n-2\\n+3\\n1')
    2
    """
    offsets = parse(text)
    frequency = 0
    seen = {frequency}
    for offset in cycle(offsets):
        frequency += offset
        if frequency in seen:
            return frequency
        seen.add(frequency)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
