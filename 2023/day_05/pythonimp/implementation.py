from bisect import bisect_right
from math import inf


class Map:
    def __init__(self, ranges, max_value=1_000_000_000):
        ranges = self.fill_in_ranges(ranges)
        self.ranges = sorted(ranges, key=lambda x: x[1])
        self.range_keys = [source for (_, source, _) in self.ranges]
        self.inverse_ranges = sorted(self.ranges, key=lambda x: x[0])
        self.inverse_range_keys = [target for (target, _, _) in self.inverse_ranges]

    def fill_in_ranges(self, ranges):
        ranges = sorted(ranges, key=lambda x: x[1])
        additional_ranges = []
        last_start = 0
        for target, source, length in ranges:
            new_length = source - last_start
            if new_length > 0:
                additional_ranges.append((last_start, last_start, new_length))
            last_start = source + length
        additional_ranges.append((last_start, last_start, inf))
        return ranges + additional_ranges

    def lookup_range(self, start, length):
        end = start + length
        i0 = bisect_right(self.range_keys, start) - 1
        i1 = bisect_right(self.range_keys, end)
        ranges = []
        for i in range(i0, i1):
            target_start, source_start, length = self.ranges[i]
            source_end = source_start + length
            new_source_start = max(start, source_start)
            new_source_end = min(end, source_end)
            if new_source_end > new_source_start:
                new_target_start = target_start + (new_source_start - source_start)
                new_target_length = new_source_end - new_source_start
                ranges.append((new_target_start, new_target_length))
        return ranges

    def lookup(self, value):
        i = bisect_right(self.range_keys, value)
        target, source, length = self.ranges[i - 1]
        delta = value - source
        if 0 <= delta < length:
            return target + delta

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


def find_seed_from_location(location, target_info):
    target = 'location'
    value = location
    while target != 'seed':
        source, mapper = target_info[target]
        value = mapper.inverse_lookup(value)
        target = source
    return value


def find_location_ranges(seed_ranges, map_info):
    source_to_target = {source: target for ((source, target), ranges) in map_info}
    assert len(source_to_target) == len(map_info), 'duplicate sources'
    source_to_map = {source: Map(ranges) for ((source, target), ranges) in map_info}
    source = 'seed'
    value = seed_ranges
    new_value = []
    while source != 'location':
        target = source_to_target[source]
        for start, length in value:
            new_value.extend(source_to_map[source].lookup_range(start, length))
        source = target
        value = new_value
        new_value = []
    return value


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    46
    """
    raw_seed_ranges, map_info = parse(text)
    seed_ranges = list(zip(raw_seed_ranges[0::2], raw_seed_ranges[1::2]))
    location_ranges = find_location_ranges(seed_ranges, map_info)
    return min(start for (start, length) in location_ranges)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
