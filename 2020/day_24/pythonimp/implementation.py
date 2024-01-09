from collections import defaultdict


def parse_row(row):
    i = 0
    while i < len(row):
        match row[i]:
            case 'e' | 'w':
                yield row[i : i + 1]
                i += 1
            case 's' | 'n':
                assert row[i : i + 2] in ('se', 'sw', 'ne', 'nw')
                yield row[i : i + 2]
                i += 2
            case _:
                raise ValueError(row[i : i + 2])


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[0][:8]
    ['se', 'se', 'nw', 'ne', 'ne', 'ne', 'w', 'se']
    """
    tile_directions = []
    for row in text.strip().split('\n'):
        tile_directions.append(list(parse_row(row)))
    return tile_directions


neighbor_offsets = {
    'e': (1, 0, -1),
    'w': (-1, 0, 1),
    'nw': (0, -1, 1),
    'se': (0, 1, -1),
    'ne': (1, -1, 0),
    'sw': (-1, 1, 0),
}


def follow(directions):
    q, r, s = 0, 0, 0
    for x in directions:
        dq, dr, ds = neighbor_offsets[x]
        q = q + dq
        r = r + dr
        s = s + ds
    return (q, r, s)


def find_black_tiles(directions):
    is_black = defaultdict(bool)
    for path in directions:
        tile = follow(path)
        is_black[tile] = not is_black[tile]
    return frozenset(k for (k, v) in is_black.items() if v)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    10
    """
    tiles = find_black_tiles(parse(text))
    return len(tiles)


def flip_tiles(tiles: frozenset) -> frozenset:
    #
    tile_counts = defaultdict(int)
    for q0, r0, s0 in tiles:
        for dq, dr, ds in neighbor_offsets.values():
            q = q0 + dq
            r = r0 + dr
            s = s0 + ds
            tile_counts[q, r, s] += 1
    new_tiles = set()
    for k in tiles:
        if tile_counts[k] in (1, 2):
            new_tiles.add(k)
    for k, v in tile_counts.items():
        if k not in tiles and v == 2:
            new_tiles.add(k)
    return frozenset(new_tiles)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2208
    """
    tiles = find_black_tiles(parse(text))
    for _ in range(100):
        tiles = flip_tiles(tiles)
    return len(tiles)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
