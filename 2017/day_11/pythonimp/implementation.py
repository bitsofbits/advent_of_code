def parse(text):
    return text.strip().split(",")


def move_from(pt, heading):
    """pt is in in qrs coordinates, see here:
    https://www.redblobgames.com/grids/hexagons/
    """
    q, r, s = pt
    match heading:
        case "n":
            return (q, r + 1, s - 1)
        case "ne":
            return (q + 1, r, s - 1)
        case "se":
            return (q + 1, r - 1, s)
        case "s":
            return (q, r - 1, s + 1)
        case "sw":
            return (q - 1, r, s + 1)
        case "nw":
            return (q - 1, r + 1, s)
        case _:
            raise ValueError(heading)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    pt = (0, 0, 0)
    for x in parse(text):
        pt = move_from(pt, x)
    return sum(abs(x) for x in pt) // 2


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3
    """
    pt = (0, 0, 0)
    furthest = 0
    for x in parse(text):
        pt = move_from(pt, x)
        distance = sum(abs(x) for x in pt) // 2
        furthest = max(distance, furthest)
    return furthest


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
