from math import lcm


def parse_line(line):
    line = line[1:-1]
    items = [x.strip().split('=') for x in line.split(',')]
    assert [k for (k, v) in items] == ['x', 'y', 'z']
    return tuple(int(v) for (k, v) in items)


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:2]
    [(-1, 0, 2), (2, -10, -7)]
    """
    return [parse_line(x.strip()) for x in text.strip().split('\n')]


def gravity_1d(a, b):
    return int(b > a) - int(b < a)


def gravity(p1, p2):
    return tuple(gravity_1d(a, b) for (a, b) in zip(p1, p2))


def step(locations, velocities):
    """
    >>> locations = parse(EXAMPLE_TEXT)
    >>> locations
    [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
    >>> velocities = [(0, 0, 0)] * len(locations)
    >>> locations, velocities = step(locations, velocities)
    >>> locations
    [(2, -1, 1), (3, -7, -4), (1, -7, 5), (2, 2, 0)]
    """
    new_velocities = []
    for p0, v0 in zip(locations, velocities):
        deltas = [v0]
        for p1 in locations:
            deltas.append(gravity(p0, p1))
        new_velocities.append(tuple(sum(x) for x in zip(*deltas)))
    new_locations = []
    for p0, v in zip(locations, new_velocities):
        new_locations.append(tuple(a + b for (a, b) in zip(p0, v)))
    return new_locations, new_velocities


def part_1(text, steps=1000):
    """
    >>> part_1(EXAMPLE_TEXT, steps=10)
    179
    """
    locations = parse(text)
    velocities = [(0, 0, 0)] * len(locations)
    for _ in range(steps):
        locations, velocities = step(locations, velocities)
    energy = 0
    for p, v in zip(locations, velocities):
        PE = sum(abs(x) for x in p)
        KE = sum(abs(x) for x in v)
        energy += PE * KE
    return energy


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2772

    543673227860472
    """
    locations = parse(text)
    velocities = [(0, 0, 0)] * len(locations)
    initial_locations = locations.copy()
    initial_velocities = velocities.copy()
    cycles = [None] * 3
    i = 0
    while any(x is None for x in cycles):
        locations, velocities = step(locations, velocities)
        i += 1
        for j in range(3):
            if cycles[j] is None:
                locations_match = all(
                    a[j] == b[j] for (a, b) in zip(locations, initial_locations)
                )
                velocities_match = all(
                    a[j] == b[j] for (a, b) in zip(velocities, initial_velocities)
                )
                if locations_match and velocities_match:
                    cycles[j] = i
    return lcm(*cycles)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
