from itertools import count


class Map:
    def __init__(self, ranges):
        self.ranges = ranges

    def lookup(self, value):
        for target, source, length in self.ranges:
            delta = value - source
            if 0 <= delta < length:
                return target + delta
        return value

    def inverse_lookup(self, value):
        for target, source, length in self.ranges:
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


def find_seed_locations(seeds, map_info):
    source_to_target = {source: target for ((source, target), ranges) in map_info}
    assert len(source_to_target) == len(map_info), 'duplicate sources'
    source_to_map = {source: Map(ranges) for ((source, target), ranges) in map_info}
    seed_to_location = {}
    for seed in seeds:
        source = 'seed'
        value = seed
        while source != 'location':
            target = source_to_target[source]
            value = source_to_map[source].lookup(value)
            source = target
        seed_to_location[seed] = value
    return seed_to_location


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
    for i0, n in zip(seed_starts, seed_lengths):
        if i0 <= x < i0 + n:
            return True
    return False


def find_seed_from_location(location, map_info):
    target_to_source = {target: source for ((source, target), ranges) in map_info}
    assert len(target_to_source) == len(map_info), 'duplicate targets'
    target_to_map = {target: Map(ranges) for ((source, target), ranges) in map_info}
    target = 'location'
    value = location
    while target != 'seed':
        source = target_to_source[target]
        value = target_to_map[target].inverse_lookup(value)
        target = source
    return value


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    46
    """
    seed_ranges, map_info = parse(text)
    seed_starts = seed_ranges[0::2]
    seed_lengths = seed_ranges[1::2]
    for location in count():
        candidate = find_seed_from_location(location, map_info)
        if seed_exists(candidate, seed_starts, seed_lengths):
            return location


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
