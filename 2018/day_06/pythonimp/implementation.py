from collections import defaultdict
from heapq import heapify, heappop, heappush


def parse(text):
    """
    >>> sorted(parse(EXAMPLE_TEXT))
    [('1', 1, 1), ('1', 1, 6), ('3', 3, 4), ('5', 5, 5), ('8', 8, 3), ('8', 8, 9)]
    """
    points = set()
    for i, line in enumerate(text.strip().split('\n')):
        i, j = (int(x.strip()) for x in line.split(','))
        label = str(i)
        points.add((label, i, j))
    return points


def parallel_flood_fill(starts, max_dist):
    fill = {}
    queue = [(0, i, j, (i, j)) for (lbl, i, j) in starts]
    inifinite_labels = set()
    heapify(queue)
    while queue:
        dist, i0, j0, lbl = heappop(queue)
        key = (i0, j0)
        if key in fill:
            existing_lbl, existing_dist = fill[key]
            if lbl != existing_lbl and dist == existing_dist:
                fill[key] = (None, existing_dist)
            assert dist >= existing_dist
            continue
        fill[key] = lbl, dist
        if dist > max_dist:
            inifinite_labels.add(lbl)
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == dj == 0:
                    continue
                i = i0 + di
                j = j0 + dj
                i00, j00 = lbl
                next_dist = abs(i - i00) + abs(j - j00)
                heappush(queue, (next_dist, i, j, lbl))
    return fill, inifinite_labels


def render(fill, start_points, inifinite_labels):
    inifinite_labels = inifinite_labels | {None}
    i0 = min(i for ((i, j), (p, _)) in fill.items() if p not in inifinite_labels)
    i1 = max(i for ((i, j), (p, _)) in fill.items() if p not in inifinite_labels) + 1
    j0 = min(j for ((i, j), (p, _)) in fill.items() if p not in inifinite_labels)
    j1 = max(j for ((i, j), (p, _)) in fill.items() if p not in inifinite_labels) + 1
    labels = {(i, j): lbl for (lbl, i, j) in start_points}
    rows = []
    for i in range(i0, i1):
        row = []
        for j in range(j0, j1):
            if (i, j) not in fill:
                row.append('•')
            else:
                start_point, dist = fill[i, j]
                if start_point is None:
                    row.append('*')
                else:
                    row.append(labels[start_point])
        rows.append(''.join(row))
    return '\n'.join(rows)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    17

    4143
    """
    start_points = parse(text)
    base_fill, inifinite_labels = parallel_flood_fill(start_points, 100)
    fill = {
        k: v
        for (k, v) in base_fill.items()
        if v[0] not in inifinite_labels and v[0] is not None
    }

    # print(render(base_fill, start_points, inifinite_labels))

    counts = defaultdict(int)
    for lbl, _ in fill.values():
        counts[lbl] += 1
    return max(counts.values())


def part_2(text, max_dist=10000):
    """
    >>> part_2(EXAMPLE_TEXT, 32)
    16

    35039
    """
    # Super duper slow. Could do this first with only x, then with only y to narrow it down,
    # then do what's left with both on much smaller area.
    start_points = parse(text)
    i0 = min(i for ((_, i, j)) in start_points)
    i1 = max(i for ((_, i, j)) in start_points) + 1
    j0 = min(j for ((_, i, j)) in start_points)
    j1 = max(j for ((_, i, j)) in start_points) + 1
    count = 0
    for i in range(i1 - max_dist, i0 + max_dist):
        for j in range(j1 - max_dist, j0 + max_dist):
            distance = sum(abs(i - i0) + abs(j - j0) for (_, i0, j0) in start_points)
            if distance < max_dist:
                count += 1
    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
