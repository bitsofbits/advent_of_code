def parse(text):
    for line in text.strip().split("\n"):
        yield line.strip()


def row_of(bp):
    """
    >>> for bp in parse(EXAMPLE_TEXT): print(row_of(bp))
    70
    14
    102
    """
    high = 128
    low = 0
    for x in bp[:7]:
        mid = low + (high - low) // 2
        if x == "F":
            high = mid
        else:
            assert x == "B"
            low = mid
    assert high == low + 1, (low, high)
    return low


def col_of(bp):
    """
    >>> for bp in parse(EXAMPLE_TEXT): print(col_of(bp))
    7
    7
    4
    """
    high = 8
    low = 0
    for x in bp[7:]:
        mid = low + (high - low) // 2
        if x == "L":
            high = mid
        else:
            assert x == "R"
            low = mid
    assert high == low + 1, (low, high)
    return low


def id_of(bp):
    return 8 * row_of(bp) + col_of(bp)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    820
    """
    return max(id_of(x) for x in parse(text))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    120
    """
    ids = set(id_of(x) for x in parse(text))
    for i in range(min(ids), max(ids) + 1):
        if i not in ids:
            return i


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
