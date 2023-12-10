from bisect import bisect_right
from itertools import count


class Map:
    def __init__(self, ranges, max_value=1_000_000_000):
        self.ranges = sorted(ranges, key=lambda x: x[1])
        self.range_keys = [source for (_, source, _) in self.ranges]
        self.inverse_ranges = sorted(self.ranges, key=lambda x: x[0])
        self.inverse_range_keys = [target for (target, _, _) in self.inverse_ranges]

    def lookup(self, value):
        i = bisect_right(self.range_keys, value)
        if 0 < i <= len(self.ranges):
            target, source, length = self.ranges[i - 1]
            delta = value - source
            if 0 <= delta < length:
                return target + delta
        return value

    def inverse_lookup(self, value):
        i = bisect_right(self.inverse_range_keys, value)
        if 0 < i <= len(self.inverse_ranges):
            target, source, length = self.inverse_ranges[i - 1]
            delta = value - target
            if 0 <= delta < length:
                return source + delta
        return value


def parse_seed_info(line):
    # seeds: 79 14 55 13
    label, seed_text = line.strip().split(': ')
    assert label == 'seeds'
    return [int(x) for x in seed_text.strip().split()]


def parse_map(text):
    # seed-to-soil map:
    # 50 98 2
    # 52 50 48
    lines = text.strip().split("\n")
    label, extra = lines[0].split()
    assert extra == 'map:'
    source, _, target = label.split('-')
    ranges = []
    for line in lines[1:]:
        line = line.strip()
        if line:
            ranges.append(tuple(int(x) for x in line.strip().split()))
    return (source, target), ranges


def parse(text):
    """
    >>> seed_info, maps = parse(EXAMPLE_TEXT)
    >>> seed_info
    [79, 14, 55, 13]
    >>> maps[0]
    (('seed', 'soil'), [(50, 98, 2), (52, 50, 48)])
    """
    blocks = text.strip().split('\n\n')
    seed_text = blocks[0]
    maps_info = blocks[1:]
    return parse_seed_info(seed_text), [parse_map(x) for x in maps_info]


def find_seed_location(seed, source_to_target, source_to_map):
    source = 'seed'
    value = seed
    while source != 'location':
        target = source_to_target[source]
        value = source_to_map[source].lookup(value)
        source = target
    return value


def find_seed_locations(seeds, map_info):
    source_to_target = {source: target for ((source, target), ranges) in map_info}
    assert len(source_to_target) == len(map_info), 'duplicate sources'
    source_to_map = {source: Map(ranges) for ((source, target), ranges) in map_info}
    return {x: find_seed_location(x, source_to_target, source_to_map) for x in seeds}


def part_1(text):
    """
    Seed 79, soil 81, fertilizer 81, ... location 82.
    Seed 14, soil 14, fertilizer 53, ... location 43.
    Seed 55, soil 57, fertilizer 57, ... location 86.
    Seed 13, soil 13, fertilizer 52, ... location 35.

    >>> part_1(EXAMPLE_TEXT)
    35
    """
    seeds, map_info = parse(text)
    seed_to_location = find_seed_locations(seeds, map_info)
    return min(seed_to_location.values())


def seed_exists(x, seed_starts, seed_lengths):
    # seed_starts must be ordered and ranges should not overlap
    i = bisect_right(seed_starts, x)
    if 0 < i <= len(seed_starts):
        start = seed_starts[i - 1]
        length = seed_lengths[i - 1]
        if start <= x < start + length:
            return True
    return False

    # for i0, n in zip(seed_starts, seed_lengths):
    #     if i0 <= x < i0 + n:
    #         return True
    # return False


def find_seed_from_location(location, target_info):
    target = 'location'
    value = location
    while target != 'seed':
        source, mapper = target_info[target]
        value = mapper.inverse_lookup(value)
        target = source
    return value


def part_2(text):
    """
    A potentially faster–but more complicated–approach would be to track ranges all the
    way through.

    >>> part_2(EXAMPLE_TEXT)
    46
    """
    seed_ranges, map_info = parse(text)
    seed_starts = seed_ranges[0::2]
    seed_lengths = seed_ranges[1::2]
    # Sort by start
    arg = sorted(range(len(seed_starts)), key=seed_starts.__getitem__)
    seed_starts = [seed_starts[i] for i in arg]
    seed_lengths = [seed_lengths[i] for i in arg]

    target_info = {
        target: (source, Map(ranges)) for ((source, target), ranges) in map_info
    }
    assert len(target_info) == len(map_info), 'duplicate targets'
    for location in count():
        candidate = find_seed_from_location(location, target_info)
        if seed_exists(candidate, seed_starts, seed_lengths):
            return location


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
