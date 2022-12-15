from numba import njit
from numba.typed import List


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
    >>> Sensor("Sensor at x=8, y=7: closest beacon is at x=2, y=10")
    Parser((8, 7), (2, 10))
    """

    def __init__(self, text):
        x, y, beacon_x, beacon_y = self.parse(text)
        self.location = (x, y)
        self.nearest_beacon = (beacon_x, beacon_y)
        self.dist = manhattan(self.location, self.nearest_beacon)

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
        x0, y0 = s.location
        dist = s.dist
        rng = dist - abs(row - y0)
        xa = x0 - rng
        xb = x0 + rng + 1
        coverage.update(range(xa, xb))
        xb, yb = s.nearest_beacon
        if yb == row:
            beacons.add(xb)
    return len(coverage - beacons)


@njit
def _find_tuning_freq(sensor_info, max_coord):
    for y in range(max_coord + 1):
        bounds = [(-1, 1), (-1, -1)]
        # Have beginning (-1) to sort before end (+1) if there's a tie
        for x0, y0, d in sensor_info:
            rng = d - abs(y - y0)
            if rng >= 0:
                xa = x0 - rng
                xb = x0 + rng + 1
                if xb >= 0 and xa <= max_coord + 1:
                    bounds.append((xa, -1))
                    bounds.append((xb, 1))
        bounds.sort()
        depth = 0
        x0, delta_0 = bounds[0]
        for x, delta in bounds:
            depth -= delta
            if x < 0:
                continue
            if x > max_coord:
                break
            if depth == 0:
                return x * 4000000 + y
    return -1


def find_tuning_freq(sensors, max_coord):
    """
    >>> sensors = load_sensors("data/example.txt")
    >>> find_tuning_freq(sensors, 20)
    56000011
    """
    sensor_info = List()
    for s in sensors:
        sensor_info.append((*s.location, s.dist))
    return _find_tuning_freq(sensor_info, max_coord)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
