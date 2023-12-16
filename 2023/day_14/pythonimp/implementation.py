def render(movable, fixed, n_rows, n_cols):
    lines = []
    for i in range(n_rows):
        line = []
        for j in range(n_cols):
            if movable[i][j]:
                line.append('O')
            elif fixed[i][j]:
                line.append('#')
            else:
                line.append('.')
        lines.append(''.join(line))
    return '\n'.join(lines)


def decompose(board, n_rows, n_cols):
    movable = [[board.get((i, j)) == 'O' for j in range(n_cols)] for i in range(n_rows)]
    fixed = [[board.get((i, j)) == '#' for j in range(n_cols)] for i in range(n_rows)]
    return movable, fixed


def parse(text):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> n_rows, n_cols
    (10, 10)
    >>> movable, fixed = decompose(board, n_rows, n_cols)
    >>> print(render(movable, fixed, n_rows, n_cols))
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


def tilt_north(movable, fixed, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> movable, fixed = decompose(board, n_rows, n_cols)
    >>> tilt_north(movable, fixed, n_rows, n_cols)
    >>> print(render(movable, fixed, n_rows, n_cols))
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
    limit = [0] * n_cols
    for i in range(n_rows):
        for j in range(n_cols):
            if movable[i][j]:
                movable[i][j] = 0
                min_i = limit[j]
                movable[min_i][j] = 1
                limit[j] = min_i + 1
            elif fixed[i][j]:
                limit[j] = i + 1


def tilt_south(movable, fixed, n_rows, n_cols):
    limit = [n_rows - 1] * n_cols
    for i in reversed(range(n_rows)):
        for j in range(n_cols):
            if movable[i][j]:
                movable[i][j] = 0
                max_i = limit[j]
                movable[max_i][j] = 1
                limit[j] = max_i - 1
            elif fixed[i][j]:
                limit[j] = i - 1


def tilt_west(movable, fixed, n_rows, n_cols):
    limit = [0] * n_rows
    for j in range(n_cols):
        for i in range(n_rows):
            if movable[i][j]:
                movable[i][j] = 0
                min_j = limit[i]
                movable[i][min_j] = 1
                limit[i] = min_j + 1
            elif fixed[i][j]:
                limit[i] = j + 1


def tilt_east(movable, fixed, n_rows, n_cols):
    limit = [n_cols - 1] * n_rows
    for j in reversed(range(n_cols)):
        for i in range(n_rows):
            if movable[i][j]:
                movable[i][j] = 0
                max_j = limit[i]
                movable[i][max_j] = 1
                limit[i] = max_j - 1
            elif fixed[i][j]:
                limit[i] = j - 1


def spin(movable, fixed, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> movable, fixed = decompose(board, n_rows, n_cols)
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> print("----------\\n", render(movable, fixed, n_rows, n_cols), sep='')
    ----------
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
    tilt_north(movable, fixed, n_rows, n_cols)
    tilt_west(movable, fixed, n_rows, n_cols)
    tilt_south(movable, fixed, n_rows, n_cols)
    tilt_east(movable, fixed, n_rows, n_cols)
    return movable


def compute_load(movable, n_rows, n_cols):
    total = 0
    for i, row in enumerate(movable):
        total += (n_rows - i) * sum(row)
    return total


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    136
    """
    board, n_rows, n_cols = parse(text)
    movable, fixed = decompose(board, n_rows, n_cols)
    tilt_north(movable, fixed, n_rows, n_cols)
    return compute_load(movable, n_rows, n_cols)


def part_2(text, spins=1000000000):
    """
    >>> part_2(EXAMPLE_TEXT, spins=1000000000)
    64
    """
    board, n_rows, n_cols = parse(text)
    movable, fixed = decompose(board, n_rows, n_cols)

    def as_key(x):
        return tuple(tuple(y) for y in x)

    states = {}
    next_key = as_key(movable)

    for n in range(1, spins + 1):
        key = next_key
        spin(movable, fixed, n_rows, n_cols)
        next_key = as_key(movable)
        if key in states:
            n0, movable = states[key]
            left = (spins - n) % (n - n0)
            for _ in range(left):
                _, movable = states[as_key(movable)]
            break
        states[key] = (n, next_key)
    return compute_load(movable, n_rows, n_cols)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
