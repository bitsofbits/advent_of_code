from collections import defaultdict

EXAMPLE_TEXT = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    198
    """
    counters = defaultdict(lambda: defaultdict(int))
    for line in text.strip().split("\n"):
        for i, c in enumerate(line.strip()):
            counters[i][c] += 1
    gamma = ""
    epsilon = ""
    for k in sorted(counters):
        cntr = counters[k]
        ordered = sorted(cntr, key=lambda x: cntr[x])
        epsilon += ordered[0]
        gamma += ordered[-1]
    epsilon = int(epsilon, base=2)
    gamma = int(gamma, base=2)
    return epsilon * gamma


def filter_by_order(lines, order):
    """
    >>> lines = EXAMPLE_TEXT.strip().split("\\n")
    >>> filter_by_order(lines, order=-1)
    '10111'
    >>> filter_by_order(lines, order=0)
    '01010'
    """
    lines = lines.copy()
    N = len(lines[0])
    for i in range(N):
        if len(lines) == 1:
            break
        cntr = defaultdict(int)
        for line in lines:
            cntr[line[i]] += 1
        ordered = sorted(cntr, key=lambda x: (cntr[x], x))
        filterval = ordered[order]
        lines = [x for x in lines if x[i] == filterval]
    [value] = lines
    return value


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    230
    """
    lines = text.strip().split("\n")
    og = int(filter_by_order(lines, order=-1), base=2)
    cs = int(filter_by_order(lines, order=0), base=2)
    return og * cs


if __name__ == "__main__":
    import doctest

    doctest.testmod()
