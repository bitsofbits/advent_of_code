import re

# position=< 20732, -51094> velocity=<-2,  5>

pattern = re.compile(r'^position=<(.*),(.*)> velocity=<(.*),(.*)>$')


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:4]
    [((9, 1), (0, 2)), ((7, 0), (-1, 0)), ((3, -2), (-1, 1)), ((6, 10), (-2, -1))]
    """
    for line in text.strip().split('\n'):
        match = pattern.match(line)
        x, y, vx, vy = (int(x.strip()) for x in match.groups())
        yield (x, y), (vx, vy)


def render(points):
    i0 = min(i for ((i, j)) in points)
    i1 = max(i for ((i, j)) in points) + 1
    j0 = min(j for ((i, j)) in points)
    j1 = max(j for ((i, j)) in points) + 1
    rows = []
    for j in range(j0, j1):
        row = []
        for i in range(i0, i1):
            row.append('#' if ((i, j) in points) else '•')
        rows.append(''.join(row))
    return '\n'.join(rows)


def rms(values):
    v0 = sum(values) / len(values)
    return (sum((v - v0) ** 2 for v in values) / len(values)) ** 0.5


def spread(points):
    return rms([x for (x, y) in points]) + rms([y for (x, y) in points])


def update(points, velocities, dt=1):
    for (i, j), (vi, vj) in zip(points, velocities):
        yield i + dt * vi, j + dt * vj


def part_1(text, high_t=20_000):
    """
    2
    ••••••••••#•••
    #••#•••####••#
    ••••••••••••••
    ••••#••••#••••
    ••#•#•••••••••
    •••#•••#••••••
    •••#••#••#•#••
    #••••#•#••••••
    •#•••#•••##•#•
    ••••#•••••••••
    <BLANKLINE>
    3
    #•••#••###
    #•••#•••#•
    #•••#•••#•
    #####•••#•
    #•••#•••#•
    #•••#•••#•
    #•••#•••#•
    #•••#••###
    <BLANKLINE>
    4
    ••••••••#••••
    ••••##•••#•#•
    ••#•••••#••#•
    •#••##•##•#••
    •••##•#••••#•
    •••••••#••••#
    ••••••••••#••
    #••••••#•••#•
    •#•••••##••••
    •••••••••••#•
    •••••••••••#•
    <BLANKLINE>
    """
    coordinates = list(parse(text))
    points = [x for (x, v) in coordinates]
    velocities = [v for (x, v) in coordinates]
    low_t = 0
    low_spread = spread(points)
    high_spread = spread(list(update(points, velocities, high_t)))
    while low_t < high_t:
        if high_t == low_t + 1:
            mid_t = low_t if (low_spread < high_spread) else high_t
            break
        mid_t = (low_t + high_t) // 2
        mid_points = list(update(points, velocities, mid_t))
        mid_spread = spread(mid_points)
        # A B C
        if low_spread < high_spread:
            high_t = mid_t
            high_spread = mid_spread
        else:
            low_t = mid_t
            low_spread = mid_spread

    for i in range(-1, 2):
        print(mid_t + i)
        print(render(list(update(points, velocities, mid_t + i))))
        print()


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
