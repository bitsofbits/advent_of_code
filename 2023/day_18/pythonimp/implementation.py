def parse(text):
    """
    # R 6 (#70c710)
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [('R', 6, '(#70c710)'), ('D', 5, '(#0dc571)')]
    """
    for line in text.strip().split('\n'):
        direction, length_str, color = line.split()
        length = int(length_str)
        yield direction, length, color


dir_to_deltas = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}


def find_trench(instructions):
    map = {(0, 0)}
    i, j = 0, 0
    for direction, length, *_ in instructions:
        di, dj = dir_to_deltas[direction]
        for n in range(length):
            i, j = i + di, j + dj
            map.add((i, j))
    return map


def find_bounds(map):
    min_i = max_i = min_j = max_j = 0
    for i, j in map:
        min_i = min(i, min_i)
        max_i = max(i, max_i)
        min_j = min(j, min_j)
        max_j = max(j, max_j)
    return min_i, max_i, min_j, max_j


def flood_fill(i0, j0, map):
    stack = [(i0, j0)]
    while stack:
        i, j = stack.pop()
        if (i, j) in map:
            continue
        map.add((i, j))
        stack.append((i + 1, j))
        stack.append((i - 1, j))
        stack.append((i, j + 1))
        stack.append((i, j - 1))


def decode_hex(text):
    """(#70c710)"""
    text = text[2:-1]  # strip '(#..)'
    length = int(text[:-1], 16)
    direction = 'RDLU'[int(text[-1])]
    return direction, length


def render(map):
    min_i, max_i, min_j, max_j = find_bounds(map)
    di = max_i - min_i + 1
    dj = max_j - min_j + 1
    lines = []
    for i in range(min_i, min_i + di):
        chars = ['#' if (i, j) in map else '.' for j in range(min_j, min_j + dj)]
        lines.append(''.join(chars))
    return '\n'.join(lines)


def guess_flood_fill_start(map):
    min_i, max_i, min_j, max_j = find_bounds(map)
    di = max_i - min_i + 1
    dj = max_j - min_j + 1
    i0 = min_i + di // 2
    j0 = min_j + dj // 2
    return i0, j0


# def compute_area(map):
#     min_i, max_i, min_j, max_j = find_bounds(map)
#     di = max_i - min_i + 1
#     dj = max_j - min_j + 1
#     for i in range()
def area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0 for ((x0, y0), (x1, y1)) in segments(p)))


def segments(p):
    return zip(p, p[1:] + [p[0]])


def as_polygon(instructions):
    poly = [(0, 0)]
    i, j = 0, 0
    for direction, length, *_ in instructions:
        di, dj = dir_to_deltas[direction]
        i += di * length
        j += dj * length
        poly.append((i, j))
    assert poly[-1] == poly[0]
    return poly[:-1]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    62.0

    43814
    """
    instructions = list(parse(text))
    poly = as_polygon(instructions)
    circumfrence = sum(x[1] for x in instructions)
    return area(poly) + circumfrence / 2 + 1
    # map = find_trench(instructions)
    # # print(render(map))
    # i0, j0 = guess_flood_fill_start(map)
    # # print()
    # flood_fill(i0, j0, map)
    # # print(render(map))
    # return len(map)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    952408144115.0
    """
    wrong_instructions = parse(text)
    instructions = [(*decode_hex(color), None) for (_, _, color) in wrong_instructions]
    poly = as_polygon(instructions)
    circumfrence = sum(x[1] for x in instructions)
    return area(poly) + circumfrence / 2 + 1


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
