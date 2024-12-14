import re
from collections import defaultdict
from itertools import count
import time
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


def move(robot, board_size):
    (p0, p1), (v0, v1) = robot
    p0 = (p0 + v0) % board_size[0]
    p1 = (p1 + v1) % board_size[1]
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
    for _ in range(100):
        for i, x in enumerate(robots):
            robots[i] = move(x, board_size)
    if debug:
        print(render(robots, board_size))

    score = 1
    di, dj = (x // 2 for x in board_size)
    for i0, i1 in [(0, di), (di + 1, board_size[0])]:
        for j0, j1 in [(0, dj), (dj + 1, board_size[1])]:
            count = sum(1 for ((i, j), _) in robots if i0 <= i < i1 and j0 <= j < j1)
            score *= count
    return score


def is_symmetric(robots, board_size):
    _, width = board_size
    max_j = width - 1
    locations = [p for (p, _) in robots]
    mirror_locations = []
    for i, j in locations:
        mirror_locations.append((i, max_j - j))
    return sorted(locations) == sorted(mirror_locations)


# # 50 i, 95 j

# for i in range(101 * 103):
#     if i % 101 == 95 and i % 103 == 50:
#         print(i)


def variance(x):
    mean = sum(x) / len(x)
    return sum((v - mean) ** 2 for v in x) / len(x)


def part_2(text, board_size=(103, 101)):
    """
    Procedure:
    1. Note that periodically pattern becomes compact
       horizontally or vertically
    2. Determine that the vertical / horizontal compactness
       first occurs at 50 / 95 steps
    3. Determine that period of vertical / horizontal
       compactness is 103 / 101
    4. Both compact when i % 101 == 95 and i % 103 == 50


    """
    robots = parse(text)
    seen_i = set()
    seen_j = set()
    i_period = j_period = None
    states = []

    for n in range(1000):
        states.append(robots.copy())
        r_i = frozenset((i, vi) for ((i, j), (vi, vj)) in robots)
        r_j = frozenset((j, vj) for ((i, j), (vi, vj)) in robots)
        if i_period is None and r_i in seen_i:
            i_period = n
        if j_period  is None and r_j in seen_j:
            j_period = n
        seen_i.add(r_i)
        seen_j.add(r_j)
        if i_period and j_period:
            break
        for i, x in enumerate(robots):
            robots[i] = move(x, board_size)

    min_variance = inf
    compact_i = -1
    for n, robots in enumerate(states[:i_period]):
        v = variance([i for ((i, j), _) in robots])
        if v < min_variance:
            min_variance = v
            compact_i = n

    min_variance = inf
    compact_j = -1
    for n, robots in enumerate(states[:j_period]):
        v = variance([j for ((i, j), _) in robots])
        if v < min_variance:
            min_variance = v
            compact_j = n

    for n in range(i_period * j_period):
        if n % i_period == compact_i and n % j_period == compact_j:
            return n


def display_tree(text, board_size=(103, 101)):
    robots = parse(text)
    for n in count():
        if n % 101 == 95 and n % 103 == 50:
            print(
                render(
                    robots, board_size, add_bar=False, background=".", foreground="*"
                )
            )
            break
        for i, x in enumerate(robots):
            robots[i] = move(x, board_size)


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
