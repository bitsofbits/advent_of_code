def parse(text):
    """
    >>> len(list(parse(EXAMPLE_TEXT)))
    6
    """
    for line in text.strip().split("\n"):
        yield int(line)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    514579
    """
    items = list(parse(text))
    for i, x in enumerate(items):
        for y in items[:i]:
            if x + y == 2020:
                return x * y


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    241861950
    """
    items = list(parse(text))
    for i, x in enumerate(items):
        for j, y in enumerate(items[:i]):
            for z in items[:j]:
                if x + y + z == 2020:
                    return x * y * z


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
