def parse(text):
    for group in text.strip().split("\n\n"):
        g = []
        for person in group.split("\n"):
            g.append(set(person))
        yield g


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    11
    """
    total = 0
    for group in parse(text):
        yes_answers = group[0]
        for person in group[1:]:
            yes_answers |= person
        total += len(yes_answers)
    return total


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    6
    """
    total = 0
    for group in parse(text):
        yes_answers = group[0]
        for person in group[1:]:
            yes_answers &= person
        total += len(yes_answers)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
