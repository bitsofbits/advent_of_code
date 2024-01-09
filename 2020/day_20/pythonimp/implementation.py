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


def get_edge(tile, edge_number):
    match edge_number:
        case 0:
            return tile[0, :]
        case 1:
            return tile[:, -1]
        case 2:
            return tile[-1, :]
        case 3:
            return tile[:, 0]
        case _:
            raise ValueError(edge_number)


def edge_keys(tile):
    for i in range(4):
        yield make_key(get_edge(tile, i))


def find_corners(tiles):
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
    return [k for (k, v) in singleton_edge_counts.items() if v == 2]


offset = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


def rotate(tile, n):
    """
    >>> tile = np.zeros([3, 3])
    >>> tile[0, 0] = 1
    >>> tile[0, -1] = 2
    >>> print(tile)
    [[1. 0. 2.]
     [0. 0. 0.]
     [0. 0. 0.]]
    >>> print(rotate(tile, 1))
    [[0. 0. 1.]
     [0. 0. 0.]
     [0. 0. 2.]]
    >>> print(rotate(tile, 2))
    [[0. 0. 0.]
     [0. 0. 0.]
     [2. 0. 1.]]
    >>> print(rotate(tile, 3))
    [[2. 0. 0.]
     [0. 0. 0.]
     [1. 0. 0.]]
    """
    tile = tile.copy()
    assert 0 <= n < 4
    match n:
        case 0:
            return tile
        case 1:
            return tile.transpose()[:, ::-1]
        case 2:
            return tile[::-1, ::-1]
        case 3:
            return tile.transpose()[::-1, :]


def get_rotations_and_flips(tile):
    for i in range(4):
        yield rotate(tile, i)
        yield rotate(tile[::-1], i)


def order(tiles):
    """
    >>> tiles = parse(EXAMPLE_TEXT)
    >>> print(len(order(tiles)))
    9
    """
    edge_map = defaultdict(set)
    for k, tile in tiles.items():
        for edge in edge_keys(tile):
            edge_map[edge].add(k)
    edge_map = dict(edge_map)
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

    used_tiles = set()
    used_locs = set()
    pending = [(id_, t, 0, 0)]
    located = []
    while pending:
        tile_id, tile, i0, j0 = pending.pop()
        if tile_id in used_tiles:
            continue
        if (i0, j0) in used_locs:
            continue
        used_tiles.add(tile_id)
        used_locs.add((i0, j0))
        located.append((tile_id, tile.copy(), i0, j0))
        for edge_number in range(4):
            edge = get_edge(tile, edge_number)
            edge_key = make_key(edge)
            for next_tile_id in edge_map[edge_key]:
                if next_tile_id in used_tiles:
                    continue
                next_tile = tiles[next_tile_id].copy()
                for transformed_tile in get_rotations_and_flips(next_tile):
                    next_edge = get_edge(transformed_tile, (edge_number + 2) % 4)
                    if np.alltrue(edge == next_edge):
                        di, dj = offset[edge_number]
                        # print(tile_id, next_tile_id, edge_number, di, dj)
                        next_i, next_j = i0 + di, j0 + dj
                        pending.append(
                            (next_tile_id, transformed_tile.copy(), next_i, next_j)
                        )
                        break

    return located


def assemble(tiles):
    """
    >>> tiles = parse(EXAMPLE_TEXT)
    >>> print(render(assemble(tiles)))
    .#.#..#.##...#.##..#####
    ###....#.#....#..#......
    ##.##.###.#.#..######...
    ###.#####...#.#####.#..#
    ##.#....#.##.####...#.##
    ...########.#....#####.#
    ....#..#...##..#.#.###..
    .####...#..#.....#......
    #..#.##..#..###.#.##....
    #.####..#.####.#.#.###..
    ###.#.#...#.######.#..##
    #.####....##..########.#
    ##..##.#...#...#.#.#.#..
    ...#..#..#.#.##..###.###
    .#.#....#.##.#...###.##.
    ###.#...#..#.##.######..
    .#.#.###.##.##.#..#.##..
    .####.###.#...###.#..#.#
    ..#.#..#..#.#.#.####.###
    #..####...#.#.#.###.###.
    #####..#####...###....##
    #.##..#..#...#..####...#
    .#.###..##..##..####.##.
    ...###...##...#...#..###
    """
    m, n = tiles[list(tiles.keys())[0]].shape
    assert m == n
    ordered_map = {(i, j): tile for (_, tile, i, j) in order(tiles)}
    size = n - 2
    i_indices = set(i for (i, j) in ordered_map)
    j_indices = set(j for (i, j) in ordered_map)
    assert min(i_indices) == min(j_indices) == 0
    M = max(i_indices) + 1
    N = max(j_indices) + 1
    board = np.zeros((M * size, N * size), dtype=int) - 1
    for i in range(M):
        for j in range(N):
            trimmed_tile = ordered_map[i, j][1:-1, 1:-1]
            board[i * size : (i + 1) * size, j * size : (j + 1) * size] = trimmed_tile
    return board


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)   # 8805021278141428867 is too high
    20899048083289
    """
    tiles = parse(text)
    corners = find_corners(tiles)
    return np.prod(corners)


mask_image = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   \
""".strip(
    '\n'
)
mask = np.zeros((3, 21), dtype=int)
for i, line in enumerate(mask_image.split('\n')):
    for j, c in enumerate(line):
        if c == "#":
            mask[i, j] = 1
inverse_mask = mask == 0


def remove_monsters(board):
    board = board.copy()
    m, n = board.shape
    M, N = mask.shape
    for i in range(m - M + 1):
        for j in range(n - N + 1):
            region = board[i : i + M, j : j + N]
            if np.alltrue(mask * region == mask):
                region *= inverse_mask
    return board


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    273
    """
    tiles = parse(text)
    board = assemble(tiles)
    min_roughness = board.sum()
    for x in get_rotations_and_flips(board):
        x = remove_monsters(x)
        if x.sum() < min_roughness:
            min_roughness = x.sum()
    return min_roughness


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
