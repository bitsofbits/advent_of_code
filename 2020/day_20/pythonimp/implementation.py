from collections import defaultdict

import numpy as np


def render(tile):
    lines = []
    for i, row in enumerate(tile):
        lines.append("".join("#" if x else "." for x in row))
    return "\n".join(lines)


def parse_tile(text):
    lines = text.strip().split("\n")
    key = int(lines[0][:-1].split()[-1])
    tile = np.zeros((10, 10), dtype=int)
    for i, line in enumerate(lines[1:]):
        for j, c in enumerate(line):
            if c == "#":
                tile[i, j] = 1
    return key, tile


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)[2971]))
    ..#.#....#
    #...###...
    #.#.###...
    ##.##..#..
    .#####..##
    .#..####.#
    #..#.#..#.
    ..####.###
    ..#.#.###.
    ...#.#.#.#
    """
    return dict(parse_tile(x) for x in text.strip().split("\n\n"))


def make_key(edge):
    return min(tuple(x) for x in [edge, edge[::-1]])


def edge_keys(tile):
    for edge in [tile[0], tile[:, 0], tile[-1], tile[:, -1]]:
        yield make_key(edge)


def order(tiles):
    edge_map = defaultdict(set)
    for k, tile in tiles.items():
        for edge in edge_keys(tile):
            edge_map[edge].add(k)
    singleton_edge_counts = defaultdict(int)
    for ids in edge_map.values():
        match tuple(ids):
            case (a,):
                singleton_edge_counts[a] += 1
            case (_, _):
                pass
            case _:
                raise ValueError(ids)
    corners = [k for (k, v) in singleton_edge_counts.items() if v == 2]
    # Pick one
    id_ = corners[0]
    t = tiles[id_]
    # and put the singleton edges on the bottom right
    counts = tuple(len(edge_map[x]) == 1 for x in edge_keys(t))
    match counts:
        case (1, 0, 0, 1):
            pass
        case (1, 1, 0, 0):
            t = t[:, ::-1]
        case (0, 1, 1, 0):
            t = t[::-1, ::-1]
        case (0, 0, 1, 1):
            t = t[::-1, :]
        case _:
            raise ValueError(counts)
    assert tuple(len(edge_map[x]) == 1 for x in edge_keys(t)) == (1, 0, 0, 1)
    #
    ordered = [[t]]
    unused = {k for k in tiles if k != id_}
    pending = [(t, 1), (t, 2)]
    # while pending
    # while unused:
    #     for k in unused:
    #         # if match(k, last[:, -1])

    return corners, ordered


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)   # 8805021278141428867 is too high
    20899048083289
    """
    tiles = parse(text)
    corners, _ = order(tiles)
    return np.prod(corners)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
