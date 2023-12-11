def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[0]
    [0, 3, 6, 9, 12, 15]
    """
    for line in text.strip().split('\n'):
        yield [int(x) for x in line.strip().split()]


def extrapolate(measurements):
    series = [measurements]
    while not all(x == 0 for x in series[-1]):
        last = series[-1]
        x0 = last[0]
        deltas = []
        for x1 in last[1:]:
            deltas.append(x1 - x0)
            x0 = x1
        series.append(deltas)
    x_0 = 0
    x_1 = 0
    for values in reversed(series):
        x_1 = values[-1] + x_1
        x_0 = values[0] - x_0
    return x_0, x_1


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    114
    """
    total = 0
    for measurements in parse(text):
        x0, x1 = extrapolate(measurements)
        total += x1
    return total


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    total = 0
    for measurements in parse(text):
        x0, x1 = extrapolate(measurements)
        # print(x0, x1)
        total += x0
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
