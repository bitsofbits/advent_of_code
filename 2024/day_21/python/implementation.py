from heapq import heappop, heappush
from itertools import pairwise
from collections import Counter
from math import inf


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ['029A', '980A', '179A', '456A', '379A']
    """
    return text.strip().split("\n")


door = {
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (1, 0): "4",
    (1, 1): "5",
    (1, 2): "6",
    (2, 0): "1",
    (2, 1): "2",
    (2, 2): "3",
    (3, 1): "0",
    (3, 2): "A",
}

robot = {(0, 1): "^", (0, 2): "A", (1, 0): "<", (1, 1): "v", (1, 2): ">"}


unit_vectors = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def find_paths_between(start, end, keymap):
    """
    >>> list(find_paths_between('7', 'A', door))[:4]
    ['>v>vv', '>>vvv', '>vvv>', 'vv>v>']
    """
    inv_map = {v: k for (k, v) in keymap.items()}
    start = inv_map[start]
    end = inv_map[end]
    queue = [(0, start, frozenset(), "")]
    while queue:
        count, loc, seen, path = heappop(queue)
        if loc == end:
            yield path
        if loc in seen:
            continue
        seen |= {loc}
        i0, j0 = loc
        count += 1
        for k, (di, dj) in unit_vectors.items():
            next_loc = (i0 + di, j0 + dj)
            if next_loc in keymap:
                heappush(queue, (count, next_loc, seen, path + k))


door_paths = {}
for start in door:
    start = door[start]
    for end in door:
        end = door[end]
        door_paths[(start, end)] = list(find_paths_between(start, end, door))

robot_paths = {}
for start in robot:
    start = robot[start]
    for end in robot:
        end = robot[end]
        robot_paths[(start, end)] = list(find_paths_between(start, end, robot))

robot_costs = {}
robot_costs[0] = {k: 1 for k in robot_paths}


def compute_robot_costs(cost_values):
    costs = {}

    for k in robot_paths:
        best_cost = inf
        for path in robot_paths[k]:
            transistions = list(pairwise("A" + path + "A"))
            best_cost = min(best_cost, sum(cost_values[x] for x in transistions))
        costs[k] = best_cost
    return costs


for i in range(25):
    robot_costs[i + 1] = compute_robot_costs(robot_costs[i])


def compute_cost(pushes, n_robots):
    """
    >>> compute_cost('029A', 0)
    12

    >>> compute_cost('029A', 1)
    28

    >>> compute_cost('029A', 2)
    68

    Check that it's fast enough
    >>> _ = compute_cost('029A', 25)
    """
    transistions = list(pairwise("A" + pushes))
    costs = robot_costs[n_robots]
    cost = 0
    for x in transistions:
        subpath_cost = inf
        for subpath in door_paths[x]:
            sub_trans = list(pairwise("A" + subpath + "A"))
            subpath_cost = min(subpath_cost, sum(costs[y] for y in sub_trans))
        cost += subpath_cost
    return cost


def part_1(text, n_robots=2):
    """
    >>> part_1(EXAMPLE_TEXT)
    126384
    """
    codes = parse(text)
    score = 0
    for code in codes:
        value = int(code.lstrip("0")[:-1])
        count = compute_cost(code, n_robots)
        score += count * value
    return score


def part_2(text):
    return part_1(text, n_robots=25)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
