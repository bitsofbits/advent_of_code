from math import inf


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [((19.0, 13.0, 30.0), (-2.0, 1.0, -2.0)), ((18.0, 19.0, 22.0), (-1.0, -1.0, -2.0))]
    """
    for line in text.strip().split("\n"):
        p_text, v_text = line.strip().split("@")
        p = tuple(float(x) for x in p_text.strip().split(', '))
        v = tuple(float(x) for x in v_text.strip().split(', '))
        yield p, v


def xy_intersect(points):
    """
    x = x1 + vx1 t
    y = y1 + vy1 t => t = (y - y1) / vy1
    => x = x1 + vx1 / vy1 (y - y1)
    or y = y1 + vy1 / vx1 (x - x1) = (y1 - vy1 / vx1 x1) + vy1 / vx1 x = ax + c

    """
    for i, (p1, v1) in enumerate(points):
        x1, y1, _ = p1
        vx1, vy1, _ = v1
        for p2, v2 in points[i + 1 :]:
            x2, y2, _ = p2
            vx2, vy2, _ = v2
            #
            a = vy1 / vx1
            b = vy2 / vx2
            c = y1 - a * x1
            d = y2 - b * x2

            if a - b != 0:
                x = (d - c) / (a - b)
                y = a * x + c
                t_a = (x - x1) / vx1
                t_b = (x - x2) / vx2

                yield x, y, t_a, t_b
            else:
                yield 0, 0, -inf, -inf


def part_1(text, min_xy=200000000000000, max_xy=400000000000000):
    """
    >>> part_1(EXAMPLE_TEXT, 7, 27)
    2

    inputs -> 14672
    """
    points = list(parse(text))
    count = 0
    for x, y, t_x, t_y in xy_intersect(points):
        if t_x >= 0 and t_y >= 0 and min_xy <= x <= max_xy and min_xy <= y <= max_xy:
            count += 1
    return count


def interseting_rock_coordinates(points):
    """
    r  = r0 + v0
    p1 = r1 + v1 t
    p2 = r2 + v2 t
    p3 = ....

    r0 + v0 t_a = r1 + v1 t_a => t_a = -(r1 - r0) / (v1 - v0), t_1 = -(r1_x - r0_x) / (v1_x - v0_x)

    r0 + v0 t_b = r

    r0 + v0 T = R + V T => (v0 I - V) T = R - r0 I

    T = inv(v0 I - V)(R - r0)

    """


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    points = list(parse(text))
    # t_1 =


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
