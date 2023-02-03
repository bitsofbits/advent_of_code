def parse(text):
    """
    >>> n, traps = parse(EXAMPLE_TEXT)
    >>> n
    10
    >>> sorted(traps)
    [1, 2, 4, 6, 7, 8, 9]
    """
    text = text.strip()
    traps = set()
    for i, c in enumerate(text):
        if c == "^":
            traps.add(i)
    return len(text), traps


def part_1(text, rows=40):
    """
    >>> part_1(EXAMPLE_TEXT, 10)
    38
    """
    n, traps = parse(text)
    count = 0
    rng = range(n)
    for _ in range(rows):
        count += len(traps)
        traps = {i for i in rng if ((i - 1) in traps) ^ ((i + 1) in traps)}
    return rows * n - count


def part_2(text):
    """
    # >>> part_2(EXAMPLE_TEXT)
    """
    return part_1(text, 400000)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
