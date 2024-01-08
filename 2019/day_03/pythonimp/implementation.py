from math import inf


def parse_segment(x):
    return x[0], int(x[1:])


def parse(text):
    """
    >>> line_1, line_2 = parse(EXAMPLE_TEXT)
    >>> line_1[:4]
    [('R', 98), ('U', 47), ('R', 26), ('D', 63)]
    >>> line_2[:4]
    [('U', 98), ('R', 91), ('D', 20), ('R', 16)]
    """
    line_1, line_2 = text.strip().split('\n')
    return (
        [parse_segment(x) for x in line_1.strip().split(',')],
        [parse_segment(x) for x in line_2.strip().split(',')],
    )


def build_track(segments):
    x, y = (0, 0)
    for direction, distance in segments:
        match direction:
            case 'R':
                dx, dy = 1, 0
            case 'L':
                dx, dy = -1, 0
            case 'U':
                dx, dy = 0, 1
            case 'D':
                dx, dy = 0, -1
            case _:
                raise ValueError(direction)
        for i in range(1, distance + 1):
            x += dx
            y += dy
            yield x, y


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    135
    """
    line_1, line_2 = parse(text)
    track_1 = {point for point in build_track(line_1)}
    smallest_distance = inf
    for point in build_track(line_2):
        if point in track_1:
            distance = sum(abs(v) for v in point)
            if distance <= smallest_distance:
                smallest_distance = distance
    return smallest_distance


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    410
    """
    line_1, line_2 = parse(text)
    track_1 = {point : i for (i, point) in enumerate(build_track(line_1))}
    smallest_delay = inf
    for i, point in enumerate(build_track(line_2)):
        if point in track_1:
            delay = track_1[point] + i + 2
            if delay <= smallest_delay:
                smallest_delay = delay
    return smallest_delay


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
