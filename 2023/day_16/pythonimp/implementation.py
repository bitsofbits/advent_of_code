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
def transform(i, j, heading, x):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> transform(0, 1, 'E', '|')
    [(1, 1, 'S'), (-1, 1, 'N')]
    """
    match (x, heading):
        case ('/', 'N'):
            return [(i, j + 1, 'E')]
        case ('/', 'S'):
            return [(i, j - 1, 'W')]
        case ('/', 'E'):
            return [(i - 1, j, 'N')]
        case ('/', 'W'):
            return [(i + 1, j, 'S')]

        case ('\\', 'N'):
            return [(i, j - 1, 'W')]
        case ('\\', 'S'):
            return [(i, j + 1, 'E')]
        case ('\\', 'E'):
            return [(i + 1, j, 'S')]
        case ('\\', 'W'):
            return [(i - 1, j, 'N')]

        case ('|', 'N'):
            return [(i - 1, j, 'N')]
        case ('|', 'S'):
            return [(i + 1, j, 'S')]
        case ('|', 'E'):
            return [(i + 1, j, 'S'), (i - 1, j, 'N')]
        case ('|', 'W'):
            return [(i + 1, j, 'S'), (i - 1, j, 'N')]

        case ('-', 'N'):
            return [(i, j - 1, 'W'), (i, j + 1, 'E')]
        case ('-', 'S'):
            return [(i, j - 1, 'W'), (i, j + 1, 'E')]
        case ('-', 'E'):
            return [(i, j + 1, 'E')]
        case ('-', 'W'):
            return [(i, j - 1, 'W')]

        case ('.', 'N'):
            return [(i - 1, j, 'N')]
        case ('.', 'S'):
            return [(i + 1, j, 'S')]
        case ('.', 'E'):
            return [(i, j + 1, 'E')]
        case ('.', 'W'):
            return [(i, j - 1, 'W')]

        case _:
            raise ValueError(i, j, heading, x)


def compute_energized(board, start):
    queue = deque([start])
    seen = {start}
    n_rows = len(board)
    n_cols = len(board[0])
    while queue:
        beam = queue.pop()
        seen.add(beam)
        i0, j0, _ = beam
        x = board[i0][j0]
        for x in transform(*beam, x):
            i, j, _ = x
            if 0 <= i < n_rows and 0 <= j < n_cols and x not in seen:
                queue.appendleft(x)
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
