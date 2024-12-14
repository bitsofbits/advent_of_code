import re
from collections import defaultdict
from itertools import count
from math import inf


def render(robots, board_size, add_bar=True, background=".", foreground=None):
    counts = defaultdict(int)
    for (i, j), _ in robots:
        counts[i, j] += 1
    rows = []
    for i in range(board_size[0]):
        row = []
        if add_bar:
            # Makes doctest happy
            row.append("|")
        for j in range(board_size[1]):
            if counts[i, j] == 0:
                row.append(background)
            else:
                if foreground:
                    row.append(foreground)
                else:
                    row.append(str(counts[i, j]))
        rows.append("".join(row))
    return "\n".join(rows)


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT), (7, 11)))
    |1.12.......
    |...........
    |...........
    |......11.11
    |1.1........
    |.........1.
    |.......1...
    """
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = []
    for row in text.strip().split("\n"):
        p0, p1, v0, v1 = (int(x) for x in pattern.match(row).groups())
        robots.append(((p1, p0), (v1, v0)))
    return robots


def move(robot, board_size, n=1):
    (p0, p1), (v0, v1) = robot
    p0 = (p0 + n * v0) % board_size[0]
    p1 = (p1 + n * v1) % board_size[1]
    return (p0, p1), (v0, v1)


def part_1(text, board_size=(103, 101), debug=False):
    """
    >>> part_1(EXAMPLE_TEXT, board_size=(7, 11), debug=True)
    |......2..1.
    |...........
    |1..........
    |.11........
    |.....1.....
    |...12......
    |.1....1....
    12

    228153786 too low
    """
    robots = parse(text)

    for i, x in enumerate(robots):
        robots[i] = move(x, board_size, 100)
        
    if debug:
        print(render(robots, board_size))

    score = 1
    di, dj = (x // 2 for x in board_size)
    for i0, i1 in [(0, di), (di + 1, board_size[0])]:
        for j0, j1 in [(0, dj), (dj + 1, board_size[1])]:
            cnt = sum(1 for ((i, j), _) in robots if i0 <= i < i1 and j0 <= j < j1)
            score *= cnt
    return score


def variance(x):
    sum_x = sum_x2 = 0
    for v in x:
        sum_x += v
        sum_x2 += v**2
    return sum_x2 / len(x) - (sum_x / len(x)) ** 2


def part_2(text, board_size=(103, 101)):
    """
    Procedure:
    1. Note that periodically pattern becomes compact
       vertically horizontally. We know these periods
       are 103 and 101 (board size) because the board
       sizes are prime
    2. Determine when vertical / horizontal compactness occurs
    3. Both compact when n % i_period == compact_i and n % j_period == compact_j


    """
    robots = parse(text)
    i_period, j_period = board_size
    max_period = max(board_size)

    min_i_variance = min_j_variance = inf
    compact_i = compact_j = -1
    for n in range(max_period):
        if n < i_period:
            v = variance([i for ((i, j), _) in robots])
            if v < min_i_variance:
                min_i_variance = v
                compact_i = n

        if n < j_period:
            v = variance([j for ((i, j), _) in robots])
            if v < min_j_variance:
                min_j_variance = v
                compact_j = n

        for i, x in enumerate(robots):
            robots[i] = move(x, board_size)

    for n in range(i_period * j_period):
        if n % i_period == compact_i and n % j_period == compact_j:
            return n


def display_tree(text, n=7569, board_size=(103, 101)):
    robots = parse(text)
    for i, x in enumerate(robots):
        robots[i] = move(x, board_size, n)
    print(render(robots, board_size, add_bar=False, background=".", foreground="*"))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "data.txt") as f:
        DATA_TEXT = f.read()

    doctest.testmod()

    display_tree(DATA_TEXT)
