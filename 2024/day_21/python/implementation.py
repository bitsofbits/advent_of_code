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

best_robot_path = {}
for end in robot.values():
    best_robot_path[end] = min(robot_paths['A', end], key=len) + 'A'


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
    >>> sum(compute_top_level_pushes_2('029A', n_robots=2).values())
    68

    >>> compute_top_level_pushes_2('029A', n_robots=2)

    # >>> compute_top_level_pushes('029A', [door_paths, robot_paths])
    # '<v<A>^>A<A>AvA^<AA>A<vAAA^>A'

    # >>> compute_top_level_pushes('029A', [door_paths, robot_paths, robot_paths])
    # '<vA<AA>^>AvAA^<A>A<v<A>^>AvA^A<vA^>A<Av<A>^>AAvA^A<v<A>A^>AAA<A>vA^A'

    # >>> compute_top_level_pushes('v<<A>>^A<A>AvA<^AA>A<vAAA>^A', [robot_paths])
    # '<vA<AA>^>AvAA^<A>A<v<A>^>AvA^A<vA^>A<v<A>^A>AAvA^A<v<A>A^>AAAvA^<A>A'

    """
    transistions = list(pairwise('A' + pushes))
    counts = {k : 0 for k in '<>v^A'}
    for x in transistions:
        best_sub_counts = {'A' : inf}
        for sub_path in door_paths[x]:
            sub_counts = dict(Counter(sub_path))
            for _ in range(n_robots):
                next_counts = {k : 0 for k in '<>v^A'}
                for k1, n1 in sub_counts.items():
                    for k2 in best_robot_path[k1]:
                        next_counts[k2] += n1
                sub_counts = next_counts
            if sum(sub_counts.values()) < sum(best_sub_counts.values()):
                # print(">>>", sub_counts)
                best_sub_counts = sub_counts
            # else:
            #     print("<<<", sub_counts, best_sub_counts)
            #     print("<<<", sum(sub_counts.values()) < sum(best_sub_counts.values()))
        for k1, n1 in best_sub_counts.items():
            counts[k1] += n1
    return counts



def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    126384
    """
    codes = parse(text)
    score = 0
    for code in codes:
        value = int(code.lstrip('0')[:-1])
        pushes = compute_top_level_pushes(code, [door_paths] + [robot_paths] * 2)
        score += len(pushes) * value
    return score

def part_2(text, n_robots=25):
    """
    # >>> part_2(EXAMPLE_TEXT, n_robots=2)
    126384
    """
    codes = parse(text)
    score = 0
    for code in codes:
        value = int(code.lstrip('0')[:-1])
        base_pushes = compute_top_level_pushes(code, [door_paths] + [robot_paths] * 2)

        ...


        score += len(base_pushes) * value
    return score

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
