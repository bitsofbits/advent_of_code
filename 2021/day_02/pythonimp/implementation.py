EXAMPLE_TEXT = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def parse(text):
    for line in text.strip().split("\n"):
        lbl, dist = line.split()
        dist = int(dist)
        match lbl:
            case "forward":
                yield (0, dist)
            case "down":
                yield (dist, 0)
            case "up":
                yield (-dist, 0)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    150
    """
    r, c = 0, 0
    for dr, dc in parse(text):
        r += dr
        c += dc
    return r * c


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    900
    """
    r, c, aim = 0, 0, 0
    for dr, dc in parse(text):
        aim += dr
        r += aim * dc
        c += dc
    return r * c


if __name__ == "__main__":
    import doctest

    doctest.testmod()
