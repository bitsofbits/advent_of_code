carts_to_tracks = {'>': '-', '<': '-', 'v': '|', '^': '|'}


def parse(text):
    tracks = {}
    carts = {}
    for i, row in enumerate(text.split('\n')):
        for j, x in enumerate(row):
            if x in '><^v':
                carts[i, j] = x
                x = carts_to_tracks[x]
            if x != ' ':
                tracks[i, j] = x
    return tracks, carts


turn_map = {
    ('/', 0): 1,
    ('/', 2): 3,
    ('/', 3): 2,
    ('/', 1): 0,
    ('\\', 0): 3,
    ('\\', 2): 1,
    ('\\', 3): 0,
    ('\\', 1): 2,
}

delta_map = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


def simulate(tracks, carts):
    while True:
        carts.sort()
        for ndx, (i, j, d, turn) in enumerate(carts):
            # Move cart
            x = tracks[i, j]
            if x == '+':
                d = (d + (turn - 1)) % 4
                turn = (turn + 1) % 3
            elif x in '/\\':
                d = turn_map[x, d]
            di, dj = delta_map[d]
            next_i, next_j = i + di, j + dj
            for i1, j1, *_ in carts:
                if (i1, j1) == (next_i, next_j):
                    carts[ndx] = (next_i, next_j, d, turn)
                    return carts, (i1, j1)
            carts[ndx] = (next_i, next_j, d, turn)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    (7, 3)


    """
    tracks, carts = parse(text)
    carts = [(i, j, '^>v<'.index(d), 0) for ((i, j), d) in carts.items()]
    _, (i, j) = simulate(tracks, carts)
    return j, i


def simulate2(tracks, carts):
    while len(carts) > 1:
        carts.sort()
        for ndx, (i, j, d, turn) in enumerate(carts):
            if turn is None:
                # this cart has crashed
                continue
            # Move cart
            x = tracks[i, j]
            if x == '+':
                d = (d + (turn - 1)) % 4
                turn = (turn + 1) % 3
            elif x in '/\\':
                d = turn_map[x, d]
            di, dj = delta_map[d]
            next_i, next_j = i + di, j + dj
            for ndx2, (i1, j1, d1, _) in enumerate(carts):
                if (i1, j1) == (next_i, next_j):
                    turn = None
                    carts[ndx2] = (i1, j1, d1, None)
                    carts[ndx] = (next_i, next_j, d, turn)
            carts[ndx] = (next_i, next_j, d, turn)
        # Remove crashed carts
        carts = [x for x in carts if x[-1] is not None]
    return carts


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    (6, 4)

    (27, 90) not right
    """
    tracks, carts = parse(text)
    carts = [(i, j, '^>v<'.index(d), 0) for ((i, j), d) in carts.items()]
    carts = simulate2(tracks, carts)
    [(i, j, *_)] = carts
    return j, i


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
