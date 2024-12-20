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
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            V = (i, j)
            if x == 'S':
                start = V
            elif x == 'E':
                end = V
            elif x == '#':
                walls.add(V)
    return start, end, frozenset(walls)

# def find_time_between(start, end, walls):
#     queue = [(0, start)]
#     seen = set()
#     while queue:
#         ps, loc = heappop(queue)
#         if loc == end:
#             return ps
#         if loc in seen:
#             continue
#         seen.add(loc)
#         ps += 1
#         i0, j0 = loc
#         for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             next_loc = (i0 + di, j0 + dj)
#             if next_loc not in walls:
#                 heappush(queue, (ps, next_loc))

@cache
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

# Find map of times from start
# Find map of times from end
# Remove wall and check




def part_1(text, return_detailed_counts=False, min_delta=100):
    """
    >>> part_1(EXAMPLE_TEXT, True, 1)
    [(2, 14), (4, 14), (6, 2), (8, 4), (10, 2), (12, 3), (20, 1), (36, 1), (38, 1), (40, 1), (64, 1)]

    >>> part_2(EXAMPLE_TEXT, True, 1, max_cheat=2)
    44
    
    """
    start, end, walls = parse(text)
    time_from_start = find_min_time_from(start, walls)
    time_without_cheating = time_from_start[end] 
    time_from_end = find_min_time_from(end, walls)
    # Cheating 2ps is equivalent to deleting one wall
    delta_times = []
    for wall in walls:
        i, j = wall
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            p1 = (i + di, j + dj)
            if p1 in walls:
                continue
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                p2 = (i + di, j + dj)
                if p2 in walls:
                    continue
                t = time_from_start.get(p1, inf) + time_from_end.get(p2, inf) + 2
                delta = time_without_cheating - t
                if delta >= min_delta:
                    delta_times.append(delta)
    if return_detailed_counts:
        return sorted(Counter(delta_times).most_common())
    else:
        return len(delta_times)





def part_2(text, return_detailed_counts=False, min_delta=100, max_cheat=20):
    """
    >>> part_2(EXAMPLE_TEXT, True, 50)
    285
    """
    start, end, walls = parse(text)
    time_from_start = find_min_time_from(start, walls)
    time_without_cheating = time_from_start[end] 
    time_from_end = find_min_time_from(end, walls)
    count = 0
    min_i = min(i for (i, j) in walls)
    max_i = max(i for (i, j) in walls)
    min_j = min(j for (i, j) in walls)
    max_j = max(j for (i, j) in walls)
    max_time = time_without_cheating - min_delta
    offsets = list(range(-max_cheat, max_cheat + 1))
    for i0 in range(min_i, max_i + 1):
        for j0 in range(min_j, max_j + 1):
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
                    if p1 in walls:
                        continue
                    t1 = time_from_end.get(p1, inf) + abs_di + abs_dj
                    if t1 <= max_time_ij:
                        count += 1

    return count




if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
