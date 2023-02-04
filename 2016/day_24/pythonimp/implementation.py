from heapq import heappop, heappush
from math import inf


def parse(text):
    """
    >>> origin, targets, walls = parse(EXAMPLE_TEXT)
    >>> origin
    (1, 1)
    >>> sorted(targets)
    [(1, 3), (1, 9), (3, 1), (3, 9)]
    >>> len(walls)
    35
    """
    walls = set()
    targets = set()
    origin = None
    for r, line in enumerate(text.strip().split("\n")):
        for c, x in enumerate(line):
            pt = (r, c)
            if x == "#":
                walls.add(pt)
            elif x == ".":
                pass
            elif x == "0":
                origin = pt
            else:
                assert x in "123456789"
                targets.add(pt)
    return origin, targets, walls


def traverse(origin, targets, walls):
    # cnt, loc, visited targets
    queue = [(0, origin, frozenset())]
    states = {}
    lowest_cnt = inf
    while queue:
        cnt, (r, c), visited = heappop(queue)
        if len(visited) == len(targets):
            lowest_cnt = min(cnt, lowest_cnt)
            continue
        next_cnt = cnt + 1
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            next_pt = (r + dr, c + dc)
            if next_pt in walls:
                continue
            if next_pt in targets:
                next_visited = visited | {next_pt}
            else:
                next_visited = visited
            key = (next_pt, next_visited)
            if states.get(key, inf) <= next_cnt:
                continue
            states[key] = next_cnt
            heappush(queue, (next_cnt, next_pt, next_visited))
    return lowest_cnt


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    14
    """
    origin, targets, walls = parse(text)
    return traverse(origin, targets, walls)


def traverse2(origin, targets, walls):
    # Now with the added requirement that we return to zero
    # cnt, loc, visited targets
    queue = [(0, origin, frozenset())]
    states = {}
    lowest_cnt = inf
    while queue:
        cnt, (r, c), visited = heappop(queue)
        if len(visited) == len(targets) + 1:
            lowest_cnt = min(cnt, lowest_cnt)
            continue
        next_cnt = cnt + 1
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            next_pt = (r + dr, c + dc)
            if next_pt in walls:
                continue
            if next_pt in targets:
                next_visited = visited | {next_pt}
            else:
                next_visited = visited
            if len(next_visited) == len(targets) and next_pt == origin:
                next_visited |= {origin}
            key = (next_pt, next_visited)
            if states.get(key, inf) <= next_cnt:
                continue
            states[key] = next_cnt
            heappush(queue, (next_cnt, next_pt, next_visited))
    return lowest_cnt


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    20
    """
    origin, targets, walls = parse(text)
    return traverse2(origin, targets, walls)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
