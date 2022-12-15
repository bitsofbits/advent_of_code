def extract(text):
    if text[-1] in ",:":
        text = text[:-1]
    text = text.split("=")[1]
    return int(text)


def manhattan(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return abs(x1 - x0) + abs(y0 - y1)


class Sensor:
    """
    >>> s = Sensor("Sensor at x=8, y=7: closest beacon is at x=2, y=10")
    >>> s
    Parser((8, 7), (2, 10))
    >>> c = s.coverage()
    >>> len(c)
    181
    >>> min(x for (x, y) in c)
    -1
    >>> min(y for (x, y) in c)
    -2
    """

    def __init__(self, text):
        x, y, beacon_x, beacon_y = self.parse(text)
        self.location = (x, y)
        self.nearest_beacon = (beacon_x, beacon_y)

    def parse(self, text):
        match text.strip().split():
            case (
                "Sensor",
                "at",
                x0str,
                y0str,
                "closest",
                "beacon",
                "is",
                "at",
                x1str,
                y1str,
            ):
                return extract(x0str), extract(y0str), extract(x1str), extract(y1str)

            case _:
                raise ValueError(text)

    def coverage(self):
        dist = manhattan(self.location, self.nearest_beacon)
        x0, y0 = self.location
        coverage = set()
        for i in range(-dist, dist + 1):
            j_range = dist - abs(i)
            for j in range(-j_range, j_range + 1):
                coverage.add((x0 + i, y0 + j))
        return coverage

    def row_coverage(self, row):
        dist = manhattan(self.location, self.nearest_beacon)
        x0, y0 = self.location
        x_range = dist - abs(row - y0)
        xa = x0 - x_range
        xb = x0 + x_range + 1
        return set(range(xa, xb))

    def bounded_row_coverage(self, row, max_coord):
        dist = manhattan(self.location, self.nearest_beacon)
        x0, y0 = self.location
        x_range = dist - abs(row - y0)
        xa = max(0, x0 - x_range)
        xb = min(x0 + x_range + 1, max_coord + 1)
        return set(range(xa, xb))

    def row_bounds(self, row, max_coord):
        dist = manhattan(self.location, self.nearest_beacon)
        x0, y0 = self.location
        x_range = dist - abs(row - y0)
        xa = max(0, x0 - x_range)
        xb = min(x0 + x_range + 1, max_coord + 1)
        return xa, max(xa, xb)

    #
    def __str__(self):
        return f"Parser({self.location}, {self.nearest_beacon})"

    __repr__ = __str__


def load_sensors(path):
    """
    >>> list(load_sensors("data/example.txt"))[:2]
    [Parser((2, 18), (-2, 15)), Parser((9, 16), (10, 16))]
    """
    with open(path) as f:
        for line in f:
            if line.strip():
                yield (Sensor(line))


def row_coverage(sensors, row):
    """
    >>> sensors = load_sensors("data/example.txt")
    >>> row_coverage(sensors, 10)
    26
    """
    coverage = set()
    beacons = set()
    for s in sensors:
        coverage |= s.row_coverage(row)
        beacons.add(s.nearest_beacon)
    coverage = coverage - set(x for (x, y) in beacons if y == row)
    return len(coverage)


def find_tuning_freq(sensors, max_coord):
    """
    >>> sensors = load_sensors("data/example.txt")
    >>> find_tuning_freq(sensors, 20)
    56000011
    """
    sensors = list(sensors)
    bounds = [None, None] * 2 * len(sensors)
    for y in range(max_coord + 1):
        del bounds[:]
        # Want b (-1) to sort before e if there's a tie
        bounds.append((0, -1))
        bounds.append((0, 1))
        for s in sensors:
            b, e = s.row_bounds(y, max_coord)
            bounds.append((b, -1))
            bounds.append((e, 1))
        bounds.sort()
        depth = 0
        for x, dd in bounds:
            depth -= dd
            if depth == 0 and 0 <= x <= max_coord:
                return x * 4000000 + y  # Need tp check next item in stack


if __name__ == "__main__":
    import doctest

    doctest.testmod()
