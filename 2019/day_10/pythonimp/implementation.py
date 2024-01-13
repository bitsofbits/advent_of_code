from collections import defaultdict
from math import atan2, gcd, inf, tau


def parse(text):
    """
    >>> sorted(parse(EXAMPLE_TEXT))[:10]
    [(0, 1), (0, 4), (0, 5), (0, 7), (0, 8), (0, 9), (0, 13), (0, 14), (0, 15), (0, 16)]
    """
    board = set()
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            if x == '#':
                board.add((i, j))
    return frozenset(board)


def visible_from(point, board):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> len(visible_from((13, 11), board))
    210
    """
    i0, j0 = point
    scales_by_slope = defaultdict(lambda: inf)
    for i, j in board:
        di = i - i0
        dj = j - j0
        if di == dj == 0:
            continue
        scale = gcd(di, dj)
        assert scale > 0
        slope = (di // scale, dj // scale)
        scales_by_slope[slope] = min(scales_by_slope[slope], scale)
    return frozenset((a * s, b * s) for ((a, b), s) in scales_by_slope.items())


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    210
    """
    board = parse(text)
    return max(len(visible_from(x, board)) for x in board)


def vaporize_order(point, board):
    i0, j0 = point
    scales_by_slope = defaultdict(list)
    for i, j in board:
        di = i - i0
        dj = j - j0
        if di == dj == 0:
            continue
        scale = gcd(di, dj)
        assert scale > 0
        slope = (di // scale, dj // scale)
        scales_by_slope[slope].append(scale)
    for v in scales_by_slope.values():
        v.sort(reverse=True)

    def angle(slope):
        a, b = slope
        return atan2(b, -a) % tau

    def process(candidates):
        for k in candidates:
            scale = scales_by_slope[k].pop()
            yield (i0 + k[0] * scale, j0 + k[1] * scale)
            if not scales_by_slope[k]:
                del scales_by_slope[k]

    while scales_by_slope:
        # Quadrant 1:
        candidates = [(a, b) for (a, b) in scales_by_slope if a < 0 and b >= 0]
        candidates.sort(key=angle)
        yield from process(candidates)
        # Quadrant 2:
        candidates = [(a, b) for (a, b) in scales_by_slope if a >= 0 and b > 0]
        candidates.sort(key=angle)
        yield from process(candidates)
        # Quadrant 3:
        candidates = [(a, b) for (a, b) in scales_by_slope if a > 0 and b <= 0]
        candidates.sort(key=angle)
        yield from process(candidates)
        # Quadrant 4:
        candidates = [(a, b) for (a, b) in scales_by_slope if a <= 0 and b < 0]
        candidates.sort(key=angle)
        yield from process(candidates)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    802
    """
    board = parse(text)
    point = max(board, key=lambda x: len(visible_from(x, board)))
    for i, x in enumerate(vaporize_order(point, board)):
        if i == 199:
            break
    return 100 * x[1] + x[0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
