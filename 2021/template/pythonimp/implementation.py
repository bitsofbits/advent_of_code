def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    """


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    """


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
