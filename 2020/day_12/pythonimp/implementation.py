from math import cos, radians, sin


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('F', 10)
    ('N', 3)
    ('F', 7)
    ('R', 90)
    ('F', 11)
    """
    for line in text.strip().split():
        line = line.strip()
        cmd = line[:1]
        arg = int(line[1:])
        yield cmd, arg


def perform(moves):
    i, j = 0, 0
    course = 0  # Measured CCW from east
    for mv in moves:
        match mv:
            case "N", x:
                i -= x
            case "E", x:
                j += x
            case "S", x:
                i += x
            case "W", x:
                j -= x
            case "L", x:
                course += x
            case "R", x:
                course -= x
            case "F", x:
                i -= x * sin(radians(course))
                j += x * cos(radians(course))
    return abs(i) + abs(j)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    25
    """
    moves = parse(text)
    return int(perform(moves))


def perform2(moves):
    a, b = 0, 0
    i, j = -1, 10
    for mv in moves:
        match mv:
            case "N", x:
                i -= x
            case "E", x:
                j += x
            case "S", x:
                i += x
            case "W", x:
                j -= x
            case "L", 90:
                i, j = -j, i
            case "L", 180:
                i, j = -i, -j
            case "L", 270:
                i, j = j, -i
            case "R", 90:
                i, j = j, -i
            case "R", 180:
                i, j = -i, -j
            case "R", 270:
                i, j = -j, i
            case "F", x:
                a += x * i
                b += x * j
            case _:
                raise ValueError(mv)
    return abs(a) + abs(b)


#        -j
#         |
# +-j =>   +-i or =>  -i-+
# |                      |
# i                      j


def part_2(text):
    """52349 too high, 54625 too high
    >>> part_2(EXAMPLE_TEXT)
    286
    """
    moves = parse(text)
    return perform2(moves)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
