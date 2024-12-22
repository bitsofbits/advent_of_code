from heapq import heappop, heappush
from itertools import pairwise
from collections import Counter
from math import inf

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ['029A', '980A', '179A', '456A', '379A']
    """
    return text.strip().split('\n')

door = {
 (0, 0) : '7',
 (0, 1) : '8',
 (0, 2) : '9',
 (1, 0) : '4',
 (1, 1) : '5',
 (1, 2) : '6',
 (2, 0) : '1',
 (2, 1) : '2',
 (2, 2) : '3',
 (3, 1) : '0',
 (3, 2) : 'A'
}

robot = {
    (0, 1) : '^',
    (0, 2) : 'A',
    (1, 0) : '<',
    (1, 1) : 'v',
    (1, 2) : '>'
}


unit_vectors = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}

def find_paths_between(start, end, keymap):
    """
    >>> list(find_paths_between('7', 'A', door))[:4]
    ['>v>vv', '>>vvv', '>vvv>', 'vv>v>']
    """
    inv_map = {v : k for (k, v) in keymap.items()}
    start = inv_map[start]
    end = inv_map[end]
    queue = [(0, start, frozenset(), '')]
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
robot_costs[0] = {k : 1 for k in robot_paths}



def compute_robot_costs(cost_values):
    costs = {}

    for k in robot_paths:
        best_cost = inf
        for path in robot_paths[k]:
            transistions = list(pairwise('A' + path + 'A'))
            best_cost = min(best_cost, sum(cost_values[x] for x in transistions))
        costs[k] = best_cost
    return costs

for i in range(25):
    robot_costs[i + 1] = compute_robot_costs(robot_costs[i]) 



def compute_top_level_pushes(pushes, path_maps, push=False, cache=None):
    """
    >>> compute_top_level_pushes('029A', [door_paths])
    '<A^A>^^AvvvA'

    >>> Counter(compute_top_level_pushes('029A', [door_paths, robot_paths, robot_paths])).most_common()
    [('A', 28), ('<', 11), ('>', 11), ('v', 9), ('^', 9)]

    >>> compute_top_level_pushes('029A', [door_paths, robot_paths])
    '<v<A>^>A<A>AvA^<AA>A<vAAA^>A'

    >>> compute_top_level_pushes('029A', [door_paths, robot_paths, robot_paths])
    '<vA<AA>^>AvAA^<A>A<v<A>^>AvA^A<vA^>A<Av<A>^>AAvA^A<v<A>A^>AAA<A>vA^A'

    >>> compute_top_level_pushes('v<<A>>^A<A>AvA<^AA>A<vAAA>^A', [robot_paths])
    '<vA<AA>^>AvAA^<A>A<v<A>^>AvA^A<vA^>A<v<A>^A>AAvA^A<v<A>A^>AAAvA^<A>A'

    """
    if push:
        pushes += 'A'

    if not path_maps:
        return pushes
    # assert pushes[-1] == 'A'
    path_map = path_maps[0]
    path_maps = tuple(path_maps[1:])
    transistions = list(pairwise('A' + pushes))
    path = ''
    for x in transistions:
        best_sub_path = None
        for sub_pushes in path_map[x]:
            sub_path = compute_top_level_pushes(sub_pushes, path_maps, 
                                                push=True, cache=cache)
            if best_sub_path is None or len(sub_path) < len(best_sub_path):
                best_sub_path = sub_path
        path += best_sub_path
    return path


def compute_top_level_pushes_2(pushes, n_robots):
    """
    >>> compute_top_level_pushes_2('029A', 0)
    12

    >>> compute_top_level_pushes_2('029A', 1)
    28

    >>> compute_top_level_pushes_2('029A', 2)
    68

    Check that it's fast enough
    >>> _ = compute_top_level_pushes_2('029A', 25)
    """
    transistions = list(pairwise('A' + pushes))
    costs = robot_costs[n_robots]
    cost = 0
    for x in transistions:
        subpath_cost = inf
        for subpath in door_paths[x]:
            sub_trans = list(pairwise('A' + subpath + 'A'))
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
        value = int(code.lstrip('0')[:-1])
        count = compute_top_level_pushes_2(code, n_robots)
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
