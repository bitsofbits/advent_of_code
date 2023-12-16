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


transform_map = {
    ('/', 'N'): [(0, 1, 'E')],
    ('/', 'S'): [(0, -1, 'W')],
    ('/', 'E'): [(-1, 0, 'N')],
    ('/', 'W'): [(1, 0, 'S')],
    ('\\', 'N'): [(0, -1, 'W')],
    ('\\', 'S'): [(0, 1, 'E')],
    ('\\', 'E'): [(1, 0, 'S')],
    ('\\', 'W'): [(-1, 0, 'N')],
    ('|', 'N'): [(-1, 0, 'N')],
    ('|', 'S'): [(1, 0, 'S')],
    ('|', 'E'): [(1, 0, 'S'), (-1, 0, 'N')],
    ('|', 'W'): [(1, 0, 'S'), (-1, 0, 'N')],
    ('-', 'N'): [(0, -1, 'W'), (0, 1, 'E')],
    ('-', 'S'): [(0, -1, 'W'), (0, 1, 'E')],
    ('-', 'E'): [(0, 1, 'E')],
    ('-', 'W'): [(0, -1, 'W')],
    ('.', 'N'): [(-1, 0, 'N')],
    ('.', 'S'): [(1, 0, 'S')],
    ('.', 'E'): [(0, 1, 'E')],
    ('.', 'W'): [(0, -1, 'W')],
}


@cache
def transform(i, j, heading, x, n_rows, n_cols):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> transform(0, 1, 'E', '|', 10, 10)
    [(1, 1, 'S')]
    """
    return [
        (i1, j1, new_heading)
        for (di, dj, new_heading) in transform_map[(x, heading)]
        if 0 <= (i1 := i + di) < n_rows and 0 <= (j1 := j + dj) < n_cols
    ]


def compute_beams(board, start):
    queue = [start]
    seen = set()
    n_rows = len(board)
    n_cols = len(board[0])
    while queue:
        beam = queue.pop()
        seen.add(beam)
        i, j, heading = beam
        for new_beam in transform(i, j, heading, board[i][j], n_rows, n_cols):
            if new_beam not in seen:
                queue.append(new_beam)
    return seen


def compute_energized(board, start):
    beams = compute_beams(board, start)
    energized = {(i, j) for (i, j, _) in beams}
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
        max_energized = max(
            max_energized, compute_energized(board, (row, n_cols - 1, 'W'))
        )
    for col in range(n_cols):
        max_energized = max(max_energized, compute_energized(board, (0, col, 'S')))
        max_energized = max(
            max_energized, compute_energized(board, (n_rows - 1, col, 'N'))
        )
    return max_energized


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
