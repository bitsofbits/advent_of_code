from collections import defaultdict
from itertools import count

EXAMPLE_TEXT = """
target area: x=20..30, y=-10..-5
"""


def _parse(text, target):
    assert text.startswith(f"{target}=")
    text = text[2:]
    return tuple(int(x) for x in text.split(".."))


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ((20, 30), (-10, -5))
    """
    text = text.strip()
    assert text.startswith("target area: ")
    text = text[len("target area: ") :]
    xstr, ystr = text.split(", ")
    return _parse(xstr, "x"), _parse(ystr, "y")


def find_heights(x_range, y_range):
    # Above max_vy the first point is past y_range
    height_map = defaultdict(set)
    max_vy = abs(y_range[0])
    for vy0 in range(-max_vy, max_vy + 1):
        vy = vy0
        y = 0
        max_y = y
        for t in count(1):
            y += vy
            max_y = max(y, max_y)
            if y <= y_range[1]:
                if y < y_range[0]:
                    break
                else:
                    height_map[t].add((vy0, max_y))
            vy -= 1
    # Above max_vx the first point is past x_range
    max_vx = x_range[1]
    max_time = max(height_map)
    heights = {}
    for vx0 in range(max_vx + 1):
        vx = vx0
        x = 0
        for t in range(1, max_time + 1):
            x += vx
            if x >= x_range[0]:
                if x > x_range[1]:
                    break
                elif t in height_map:
                    for vy0, max_y in height_map[t]:
                        heights[vx0, vy0] = max(max_y, heights.get((vx0, vy0), 0))
            vx = max(vx - 1, 0)
    return heights


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    45

    3570
    """
    x_range, y_range = parse(text)
    heights = find_heights(x_range, y_range)
    return max(heights.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    112
    """
    x_range, y_range = parse(text)
    heights = find_heights(x_range, y_range)
    return len(heights)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
