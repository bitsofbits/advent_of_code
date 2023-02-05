def parse(text):
    for line in text.strip().split("\n"):
        yield line.strip().split()


def is_valid_1(phrase):
    return len(set(phrase)) == len(phrase)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    return sum(1 for phrase in parse(text) if is_valid_1(phrase))


def is_valid_2(phrase):
    return len(set(tuple(sorted(x)) for x in phrase)) == len(phrase)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    return sum(1 for phrase in parse(text) if is_valid_2(phrase))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
