def render(board):
    m = max(i for (i, j) in board) + 1
    n = max(j for (i, j) in board) + 1
    lines = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(str(board[(i, j)]))
        lines.append(''.join(row))
    return '\n'.join(lines)

def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)))
    0123
    1234
    8765
    9876
    """
    board = {}
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            board[i, j] = int(x)
    return board

def find_trail_ends_from(start, board):
    stack = [(start, board[start])]
    seen = {start}
    while stack:
        (i, j), height = stack.pop()
        if height == 9:
            yield (i, j)
            continue
        for (di, dj) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_ij = i + di, j + dj
            next_height = height + 1
            if next_ij not in seen and board.get(next_ij) == next_height:
                seen.add(next_ij)
                stack.append((next_ij, next_height))


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1
    >>> part_1(EXAMPLE2_TEXT)
    36
    """
    board = parse(text)
    paths = []
    for start in sorted(k for (k, v) in board.items() if v == 0):
        for end in find_trail_ends_from(start, board):
            paths.append((start, end))
    return len(paths)


def find_trails_from(start, board):
    stack = [(start, (start,), board[start])]
    seen = {(start,)}
    while stack:
        (i, j), path, height = stack.pop()
        if height == 9:
            yield path
            continue
        for (di, dj) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_ij = i + di, j + dj
            next_path = path + (next_ij,)
            next_height = height + 1
            if next_path not in seen and board.get(next_ij) == next_height:
                seen.add(next_path)
                stack.append((next_ij, next_path, next_height))


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    81
    """
    board = parse(text)
    paths = []
    for start in sorted(k for (k, v) in board.items() if v == 0):
        for end in find_trails_from(start, board):
            paths.append((start, end))
    return len(paths)

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example_2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
