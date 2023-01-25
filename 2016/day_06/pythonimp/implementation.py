from collections import Counter


def parse(text):
    """
    >>> len(list(parse(EXAMPLE_TEXT)))
    16
    """
    for line in text.strip().split("\n"):
        yield line.strip()


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    'easter'
    """
    counters = None
    for line in parse(text):
        if counters is None:
            counters = [Counter() for _ in line]
        for c, x in zip(counters, line):
            c.update([x])
    return "".join(c.most_common(1)[0][0] for c in counters)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    'advent'
    """
    counters = None
    for line in parse(text):
        if counters is None:
            counters = [Counter() for _ in line]
        for c, x in zip(counters, line):
            c.update([x])
    return "".join(c.most_common()[-1][0] for c in counters)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
