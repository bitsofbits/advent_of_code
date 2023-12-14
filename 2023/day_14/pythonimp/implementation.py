from functools import cache


def render(board, n_rows, n_cols):
    lines = []
    for i in range(n_rows):
        line = []
        for j in range(n_cols):
            line.append(board.get((i, j), '.'))
        lines.append(''.join(line))
    return '\n'.join(lines)


def render2(movable, fixed, n_rows, n_cols):
    lines = []
    for i in range(n_rows):
        line = []
        for j in range(n_cols):
            if (i, j) in movable:
                line.append('O')
            elif (i, j) in fixed:
                line.append('#')
            else:
                line.append('.')
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


def tilt_north(movable, fixed, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> movable = set(k for k in board if board[k] == 'O')
    >>> fixed = set(k for k in board if board[k] == '#')
    >>> movable = tilt_north(movable, fixed, n_rows, n_cols)
    >>> print(render2(movable, fixed, n_rows, n_cols))
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
    limit = [0] * n_rows
    for i in range(n_rows):
        for j in range(n_cols):
            if (i, j) in movable:
                movable.remove((i, j))
                movable.add((limit[j], j))
                limit[j] += 1
            elif (i, j) in fixed:
                limit[j] = i + 1
    return movable


def tilt_south(movable, fixed, n_rows, n_cols):
    limit = [n_rows - 1] * n_rows
    for i in reversed(range(n_rows)):
        for j in range(n_cols):
            if (i, j) in movable:
                movable.remove((i, j))
                movable.add((limit[j], j))
                limit[j] -= 1
            elif (i, j) in fixed:
                limit[j] = i - 1
    return movable


def tilt_west(movable, fixed, n_rows, n_cols):
    limit = [0] * n_cols
    for j in range(n_cols):
        for i in range(n_rows):
            if (i, j) in movable:
                movable.remove((i, j))
                movable.add((i, limit[i]))
                limit[i] += 1
            elif (i, j) in fixed:
                limit[i] = j + 1
    return movable


def tilt_east(movable, fixed, n_rows, n_cols):
    limit = [n_cols - 1] * n_rows
    for j in reversed(range(n_cols)):
        for i in range(n_rows):
            if (i, j) in movable:
                movable.remove((i, j))
                movable.add((i, limit[i]))
                limit[i] -= 1
            elif (i, j) in fixed:
                limit[i] = j - 1
    return movable


def spin(movable, fixed, n_rows, n_cols):
    """
    >>> board, n_rows, n_cols = parse(EXAMPLE_TEXT)
    >>> movable = set(k for k in board if board[k] == 'O')
    >>> fixed = set(k for k in board if board[k] == '#')
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> movable = spin(movable, fixed, n_rows, n_cols)
    >>> print("-\\n", render2(movable, fixed, n_rows, n_cols), sep='')
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
    movable = tilt_north(movable, fixed, n_rows, n_cols)
    movable = tilt_west(movable, fixed, n_rows, n_cols)
    movable = tilt_south(movable, fixed, n_rows, n_cols)
    movable = tilt_east(movable, fixed, n_rows, n_cols)
    return movable


def load(movable, n_rows, n_cols):
    total = 0
    for i, j in movable:
        total += i
    return n_rows * len(movable) - total


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    136
    """
    board, n_rows, n_cols = parse(text)
    movable = set(k for k in board if board[k] == 'O')
    fixed = set(k for k in board if board[k] == '#')
    movable = tilt_north(movable, fixed, n_rows, n_cols)
    return load(movable, n_rows, n_cols)


def part_2(text, spins=1000000000):
    """
    >>> part_2(EXAMPLE_TEXT, spins=1000000000)
    64
    """
    board, n_rows, n_cols = parse(text)
    movable = set(k for k in board if board[k] == 'O')
    fixed = set(k for k in board if board[k] == '#')
    state_to_n = {frozenset(movable): 0}
    for n in range(1, spins + 1):
        movable = spin(movable, fixed, n_rows, n_cols)
        key = frozenset(movable)
        if key in state_to_n:
            delta = n - state_to_n[key]
            left = (spins - n) % delta
            for _ in range(left):
                movable = spin(movable, fixed, n_rows, n_cols)
            break
        else:
            state_to_n[key] = n
    return load(movable, n_rows, n_cols)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
