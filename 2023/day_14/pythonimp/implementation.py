from functools import cache


def render(board, n_rows, n_cols):
    lines = []
    for i in range(n_rows):
        line = []
        for j in range(n_cols):
            line.append(board.get((i, j), '.'))
        lines.append(''.join(line))
    return '\n'.join(lines)


def parse(text):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> n_rows, n_cols
    (10, 10)
    >>> print(render(board, n_rows, n_cols))
    O....#....
    O.OO#....#
    .....##...
    OO.#O....O
    .O.....O#.
    O.#..O.#.#
    ..O..#O..O
    .......O..
    #....###..
    #OO..#....
    """
    board = {}
    n_rows = 0
    for i, line in enumerate(text.strip().split('\n')):
        n_rows += 1
        n_cols = 0
        for j, x in enumerate(line):
            n_cols += 1
            if x != '.':
                board[i, j] = x
    return board, n_rows, n_cols


# @cache
def tilt_north(items, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> items = set(board.items())
    >>> items = tilt_north(items, n_rows, n_cols)
    >>> print(render(dict(items), n_rows, n_cols))
    OOOO.#.O..
    OO..#....#
    OO..O##..O
    O..#.OO...
    ........#.
    ..#....#.#
    ..O..#.O.O
    ..O.......
    #....###..
    #....#....
    """
    # items = set(items)
    limit = [0] * n_rows
    for i in range(n_rows):
        for j in range(n_cols):
            if ((i, j), 'O') in items:
                items.remove(((i, j), 'O'))
                items.add(((limit[j], j), 'O'))
                limit[j] += 1
            elif ((i, j), '#') in items:
                limit[j] = i + 1
    return items


# @cache
def tilt_south(items, n_rows, n_cols):
    items = set(((n_rows - i - 1, j), x) for ((i, j), x) in items)
    items = tilt_north(items, n_rows, n_cols)
    items = set(((n_rows - i - 1, j), x) for ((i, j), x) in items)
    return items


# @cache
def tilt_west(items, n_rows, n_cols):
    items = set(((j, i), x) for ((i, j), x) in items)
    items = tilt_north(items, n_rows, n_cols)
    items = set(((j, i), x) for ((i, j), x) in items)
    return items


# @cache
def tilt_east(items, n_rows, n_cols):
    items = set(((n_rows - j - 1, i), x) for ((i, j), x) in items)
    items = tilt_north(items, n_rows, n_cols)
    items = set(((j, n_rows - i - 1), x) for ((i, j), x) in items)
    return items


@cache
def spin(items, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> items = frozenset(board.items())
    >>> items = spin(items, n_rows, n_cols)
    >>> items = spin(items, n_rows, n_cols)
    >>> items = spin(items, n_rows, n_cols)
    >>> print("-\\n", render(dict(items), n_rows, n_cols), sep='')
    -
    .....#....
    ....#...O#
    .....##...
    ..O#......
    .....OOO#.
    .O#...O#.#
    ....O#...O
    .......OOO
    #...O###.O
    #.OOO#...O

    """
    items = set(items)
    items = tilt_north(items, n_rows, n_cols)
    items = tilt_west(items, n_rows, n_cols)
    items = tilt_south(items, n_rows, n_cols)
    items = tilt_east(items, n_rows, n_cols)
    return frozenset(items)


def load(board, n_rows, n_cols):
    total = 0
    for (i, j), x in board.items():
        if x == 'O':
            total += n_rows - i
    return total


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    136
    """
    board, n_rows, n_cols = parse(text)
    items = set(board.items())
    items = tilt_north(items, n_rows, n_cols)
    return load(dict(items), n_rows, n_cols)


def part_2(text, spins=1000000000):
    """
    >>> part_2(EXAMPLE_TEXT, spins=1000000000)
    64
    """
    board, n_rows, n_cols = parse(text)
    items = frozenset(board.items())
    seen = {items: 0}
    for i in range(spins):
        items = spin(items, n_rows, n_cols)
        n = i + 1
        if items in seen:
            delta = n - seen[items]
            left = (spins - n) % delta
            for _ in range(left):
                items = spin(items, n_rows, n_cols)
            break
        else:
            seen[items] = n
    return load(dict(items), n_rows, n_cols)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
