from collections import defaultdict


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ([3, 4, 2, 1, 3, 3], [4, 3, 5, 3, 9, 3])
    """
    list_1 = []
    list_2 = []
    for line in text.strip().split('\n'):
        a, b = line.split()
        list_1.append(int(a))
        list_2.append(int(b))
    return list_1, list_2


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    11
    """
    list_1, list_2 = parse(text)
    list_1.sort()
    list_2.sort()
    total = 0
    for x1, x2 in zip(list_1, list_2, strict=True):
        total += abs(x1 - x2)
    return total


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    31
    """
    list_1, list_2 = parse(text)
    l2_counts = defaultdict(int)
    for x in list_2:
        l2_counts[x] += 1
    score = 0
    for x in list_1:
        score += x * l2_counts[x]
    return score


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
