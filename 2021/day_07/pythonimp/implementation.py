EXAMPLE_TEXT = """
16,1,2,0,4,2,7,1,2,14
"""


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    37
    """
    locs = [int(x) for x in text.strip().split(",")]
    costs = []
    for x0 in range(min(locs), max(locs) + 1):
        costs.append(sum(abs(x - x0) for x in locs))
    return min(costs)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    168
    """
    locs = [int(x) for x in text.strip().split(",")]
    costs = []
    table = [0]
    for i in range(max(locs) - min(locs) + 1):
        table.append(table[-1] + i + 1)
    for x0 in range(min(locs), max(locs) + 1):
        costs.append(sum(table[abs(x - x0)] for x in locs))
    return min(costs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
