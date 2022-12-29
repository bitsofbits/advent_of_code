from collections import defaultdict

EXAMPLE_TEXT = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def parse(text):
    """
    >>> pairs = parse(EXAMPLE_TEXT)
    >>> pairs[1]
    ((8, 0), (0, 8))
    """
    pairs = []
    for line in text.strip().split("\n"):
        start, arrow, end = line.split()
        assert arrow == "->"
        start = tuple(int(x) for x in start.split(","))
        end = tuple(int(x) for x in end.split(","))
        pairs.append((start, end))
    return pairs


def count_overlaps(text, diagonal):
    pairs = parse(text)
    counts = defaultdict(int)
    for (i0, j0), (i1, j1) in pairs:
        if diagonal or i0 == i1 or j0 == j1:
            di = i1 - i0
            dj = j1 - j0
            steps = max(abs(di), abs(dj))
            for n in range(steps + 1):
                i = i0 + n * di // steps
                j = j0 + n * dj // steps
                counts[i, j] += 1
    return sum(1 for v in counts.values() if v > 1)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5
    """
    return count_overlaps(text, False)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    12
    """
    return count_overlaps(text, True)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
