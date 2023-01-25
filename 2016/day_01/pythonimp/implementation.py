def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:4]
    [('R', 1), ('R', 3), ('L', 2), ('L', 5)]
    """
    strings = [x.strip() for x in text.strip().split(",")]
    return [(x[0], int(x[1:])) for x in strings]


def to_grid(n, angle):
    match angle:
        case 0:
            return 0, n
        case 90:
            return n, 0
        case 180:
            return 0, -n
        case 270:
            return -n, 0
        case _:
            raise ValueError(angle)


def part_1(text):
    """
    >>> part_1("R2, L3")
    5
    >>> part_1("R2, R2, R2")
    2
    >>> part_1("R5, L5, R5, R3")
    12
    """
    x = y = 0
    angle = 0
    for turn, dist in parse(text):
        match turn:
            case "R":
                angle += 90
            case "L":
                angle -= 90
            case _:
                raise ValueError(turn)
        angle %= 360
        dx, dy = to_grid(dist, angle)
        x += dx
        y += dy
    return abs(x) + abs(y)


def sign(x):
    return (x > 0) - (x < 0)


def part_2(text):
    """
    >>> part_2("R8, R4, R4, R8")
    4
    """
    x = y = 0
    angle = 0
    visited = set([(x, y)])
    for turn, dist in parse(text):
        match turn:
            case "R":
                angle += 90
            case "L":
                angle -= 90
            case _:
                raise ValueError(turn)
        angle %= 360
        dx, dy = to_grid(dist, angle)
        for i in range(max(abs(dx), abs(dy))):
            x += sign(dx)
            y += sign(dy)
            if (x, y) in visited:
                return abs(x) + abs(y)
            visited.add((x, y))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
