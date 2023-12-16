from collections import deque
from functools import cache


def parse(text):
    """
    >>> board = parse(EXAMPLE_TEXT)
    """
    board = []
    lines = text.strip().split()
    n_rows = len(lines)
    board = [[] for _ in range(n_rows)]
    for i, row in enumerate(text.strip().split()):
        for x in row:
            board[i].append(x)
    return tuple(tuple(x) for x in board)


@cache
def transform_core(heading, x):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> transform_core('E', '|')
    [(1, 0, 'S'), (-1, 0, 'N')]
    """
    match (x, heading):
        case ('/', 'N'):
            return [(0, 1, 'E')]
        case ('/', 'S'):
            return [(0, -1, 'W')]
        case ('/', 'E'):
            return [(-1, 0, 'N')]
        case ('/', 'W'):
            return [(1, 0, 'S')]

        case ('\\', 'N'):
            return [(0, -1, 'W')]
        case ('\\', 'S'):
            return [(0, 1, 'E')]
        case ('\\', 'E'):
            return [(1, 0, 'S')]
        case ('\\', 'W'):
            return [(-1, 0, 'N')]

        case ('|', 'N'):
            return [(-1, 0, 'N')]
        case ('|', 'S'):
            return [(1, 0, 'S')]
        case ('|', 'E'):
            return [(1, 0, 'S'), (-1, 0, 'N')]
        case ('|', 'W'):
            return [(1, 0, 'S'), (-1, 0, 'N')]

        case ('-', 'N'):
            return [(0, -1, 'W'), (0, 1, 'E')]
        case ('-', 'S'):
            return [(0, -1, 'W'), (0, 1, 'E')]
        case ('-', 'E'):
            return [(0, 1, 'E')]
        case ('-', 'W'):
            return [(0, -1, 'W')]

        case ('.', 'N'):
            return [(-1, 0, 'N')]
        case ('.', 'S'):
            return [(1, 0, 'S')]
        case ('.', 'E'):
            return [(0, 1, 'E')]
        case ('.', 'W'):
            return [(0, -1, 'W')]

        case _:
            raise ValueError(i, j, heading, x)


@cache
def transform(i, j, heading, x, n_rows, n_cols):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> transform(0, 1, 'E', '|', 10, 10)
    [(1, 1, 'S')]
    """
    value = []
    for di, dj, new_heading in transform_core(heading, x):
        i1 = i + di
        j1 = j + dj
        if 0 <= i1 < n_rows and 0 <= j1 < n_cols:
            value.append((i1, j1, new_heading))
    return value



def compute_energized(board, start):
    queue = deque([start])
    seen = {start}
    n_rows = len(board)
    n_cols = len(board[0])
    while queue:
        beam = queue.pop()
        seen.add(beam)
        i, j, heading = beam
        for new_beam in transform(i, j, heading, board[i][j], n_rows, n_cols):
            if new_beam not in seen:
                queue.appendleft(new_beam)
    energized = set()
    for i, j, _ in seen:
        energized.add((i, j))
    return len(energized)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    46
    """
    board = parse(text)
    return compute_energized(board, (0, 0, 'E'))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    51
    """
    board = parse(text)
    n_rows = len(board)
    n_cols = len(board[0])
    max_energized = 0
    for row in range(n_rows):
        max_energized = max(max_energized, compute_energized(board, (row, 0, 'E')))
        max_energized = max(max_energized, compute_energized(board, (row, n_cols - 1, 'W')))
    for col in range(n_cols):
        max_energized = max(max_energized, compute_energized(board, (0, col, 'S')))
        max_energized = max(max_energized, compute_energized(board, (n_rows - 1, col, 'N')))
    return max_energized


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
