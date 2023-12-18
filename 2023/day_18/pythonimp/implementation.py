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


def area(polygon):
    total = 0
    x0, y0 = polygon[-1]
    for x1, y1 in polygon:
        total += x1 * y0 - x0 * y1
        x0, y0 = x1, y1
    return 0.5 * total


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


def instructions_to_area(instructions):
    instructions = list(instructions)
    poly = as_polygon(instructions)
    # This is the area inside the midpoint of each cell
    cross_product_area = area(poly)
    # To get the true area we need to add half the perimeter
    perimeter = sum(x[1] for x in instructions)
    # But there is an extra 1 arises because
    # we get a net extra of 4 1/4 squares at the corners. For complex shapes
    # there will be some squares with extra and some with missing 1/4 cells,
    # but they cancel out leaving a net of +1.
    return cross_product_area + perimeter / 2 + 1
    # You can also get to the above result using Pick's theorem:
    # area = interior_area + perimeter
    # cross_product_area = interior_area + perimeter / 2 - 1 (Pike's theorem)
    # => interior_area = cross_product_area - perimeter / 2 + 1
    # => area = cross_product_area + perimeter / 2 + 1


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    62

    43814
    """
    instructions = parse(text)
    return int(instructions_to_area(instructions))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    952408144115
    """
    wrong_instructions = parse(text)
    instructions = [(*decode_hex(color), None) for (_, _, color) in wrong_instructions]
    return int(instructions_to_area(instructions))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
