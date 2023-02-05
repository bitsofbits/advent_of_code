def parse(text):
    for line in text.strip().split("\n"):
        yield [int(x) for x in line.strip().split()]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    18
    """
    checksum = 0
    for row in parse(text):
        checksum += max(row) - min(row)
    return checksum


EXAMPLE2_TEXT = """
5 9 2 8
9 4 7 3
3 8 6 5
"""


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    9
    """
    total = 0
    for row in parse(text):
        for i, x in enumerate(row):
            for y in row[:i]:
                if x % y == 0:
                    total += x // y
                elif y % x == 0:
                    total += y // x
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
