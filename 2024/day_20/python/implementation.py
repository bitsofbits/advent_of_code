from heapq import heappush, heappop
from collections import Counter
from math import inf
from functools import cache


def parse(text):
    """
    >>> start, end, walls = parse(EXAMPLE_TEXT)
    >>> start, end, len(walls)
    ((3, 1), (7, 5), 140)
    """
    start = end = None
    walls = set()
    for i, row in enumerate(text.strip().split("\n")):
        for j, x in enumerate(row):
            V = (i, j)
            if x == "S":
                start = V
            elif x == "E":
                end = V
            elif x == "#":
                walls.add(V)
    return start, end, frozenset(walls)


def find_min_time_from(start, walls):
    queue = [(0, start)]
    times = {}
    while queue:
        time, loc = heappop(queue)
        if loc in times:
            continue
        times[loc] = time
        time += 1
        i0, j0 = loc
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_loc = (i0 + di, j0 + dj)
            if next_loc not in walls:
                heappush(queue, (time, next_loc))
    return times


def find_delta_times(text, min_delta, max_cheat):
    start, end, walls = parse(text)
    time_from_start = find_min_time_from(start, walls)
    time_without_cheating = time_from_start[end]
    delta_times = []
    max_time = time_without_cheating - min_delta
    offsets = list(range(-max_cheat, max_cheat + 1))
    for i0, j0 in time_from_start:
        p0 = (i0, j0)
        if p0 in walls:
            continue
        t0 = time_from_start[p0]
        if t0 > max_time:
            continue
        max_time_ij = max_time - t0
        for di in offsets:
            abs_di = abs(di)
            i1 = i0 + di
            max_abs_dj = max_cheat - abs_di
            for dj in offsets:
                abs_dj = abs(dj)
                if abs_dj > max_abs_dj:
                    continue
                p1 = (i1, j0 + dj)
                if p1 not in time_from_start:
                    continue
                t1 = time_without_cheating - time_from_start[p1] + abs_di + abs_dj
                if t1 <= max_time_ij:
                    delta_times.append(time_without_cheating - (t1 + t0))
    return delta_times


def part_1(text, return_detailed_counts=False, min_delta=100):
    """
    >>> part_1(EXAMPLE_TEXT, True, 1)
    [(2, 14), (4, 14), (6, 2), (8, 4), (10, 2), (12, 3), (20, 1), (36, 1), (38, 1), (40, 1), (64, 1)]

    >>> part_2(EXAMPLE_TEXT, min_delta=1, max_cheat=2)
    44

    """
    delta_times = find_delta_times(text, min_delta=min_delta, max_cheat=2)
    if return_detailed_counts:
        return sorted(Counter(delta_times).most_common())
    else:
        return len(delta_times)


def part_2(text, min_delta=100, max_cheat=20):
    """
    >>> part_2(EXAMPLE_TEXT, min_delta=50)
    285
    """
    return len(find_delta_times(text, min_delta=min_delta, max_cheat=max_cheat))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
