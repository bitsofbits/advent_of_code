from collections import defaultdict
from itertools import count


def render(board):
    i0 = min(i for ((i, j)) in board)
    i1 = max(i for ((i, j)) in board) + 1
    j0 = min(j for ((i, j)) in board)
    j1 = max(j for ((i, j)) in board) + 1
    rows = []
    for i in range(i0, i1):
        row = []
        for j in range(j0, j1):
            row.append(board[i, j])
        rows.append(''.join(row))
    return '\n'.join(rows)


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)))
    .#.#...|#.
    .....#|##|
    .|..|...#.
    ..|#.....#
    #.#|||#|#|
    ...#.||...
    .|....|...
    ||...#|.#|
    |.||||..|.
    ...#.|..|.
    """
    board = {}
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            board[i, j] = x
    return board


def compute_next_state(board):
    adjacent_trees = defaultdict(int)
    adjacent_yards = defaultdict(int)
    for (i, j), x in board.items():
        if x == '.':
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == dj == 0:
                    continue
                if x == '|':
                    adjacent_trees[i + di, j + dj] += 1
                elif x == '#':
                    adjacent_yards[i + di, j + dj] += 1
                else:
                    raise ValueError(x)
    next_board = {}
    for key, x in board.items():
        if x == '.':
            next_board[key] = '|' if (adjacent_trees[key] >= 3) else '.'
        elif x == '|':
            next_board[key] = '#' if (adjacent_yards[key] >= 3) else '|'
        elif x == '#':
            next_board[key] = (
                '#' if (adjacent_yards[key] >= 1 and adjacent_trees[key] >= 1) else '.'
            )
        else:
            raise ValueError(x)
    return next_board


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    .||##.....
    ||###.....
    ||##......
    |##.....##
    |##.....##
    |##....##|
    ||##.####|
    ||#####|||
    ||||#|||||
    ||||||||||
    1147
    """
    board = parse(text)
    for i in range(10):
        board = compute_next_state(board)
    print(render(board))
    return sum(x == '#' for x in board.values()) * sum(x == '|' for x in board.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    0

    208080
    """
    minutes = 1_000_000_000
    states = {}
    board = parse(text)
    for t in count():
        state = frozenset(board.items())
        if state in states:
            break
        else:
            states[state] = t
        board = compute_next_state(board)
    period = t - states[state]
    remaining = (minutes - t) % period
    for t in range(remaining):
        board = compute_next_state(board)
    return sum(x == '#' for x in board.values()) * sum(x == '|' for x in board.values())


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
