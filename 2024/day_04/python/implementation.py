def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:3]
    ['MMMSXXMASM', 'MSAMXMSMSA', 'AMXSXMAAMM']
    """
    return text.strip().split('\n')


def find_size(board):
    return len(board), len(board[0])


def count_xmas_at(i, j, board):
    """Count XMAS with 'X' at location i, j

    >>> board = parse(EXAMPLE_TEXT)
    >>> count_xmas_at(0, 4, board)
    1
    """
    h, w = find_size(board)
    count = 0
    for di, dj in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        (i1, j1) = (i, j)
        for n, x in enumerate('XMAS'):
            if not 0 <= i1 < h:
                break
            if not 0 <= j1 < w:
                break
            if board[i1][j1] != x:
                break
            i1 += di
            j1 += dj
        else:
            count += 1
    return count


def has_crossed_mas_at(i, j, board):
    """Is there a pair of MAS in X shape at location i, j

    >>> board = parse(EXAMPLE_TEXT)
    >>> has_crossed_mas_at(1, 2, board)
    1
    """
    if board[i][j] != 'A':
        return 0
    h, w = find_size(board)
    for dse in [-1, 1]:
        for dsw in [-1, 1]:
            for n, x in zip([-1, 0, 1], 'MAS'):
                i1 = i + dse * n
                j1 = j + dse * n
                if not (0 <= i1 < h and 0 <= j1 < w):
                    break
                if board[i1][j1] != x:
                    break
                i2 = i + dsw * n
                j2 = j - dsw * n
                if not (0 <= i2 < h and 0 <= j2 < w):
                    break
                if board[i2][j2] != x:
                    break
            else:
                return 1
    return 0


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    18
    """
    board = parse(text)
    h, w = find_size(board)
    count = 0
    for i in range(h):
        for j in range(w):
            count += count_xmas_at(i, j, board)
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    9
    """
    board = parse(text)
    h, w = find_size(board)
    count = 0
    for i in range(h):
        for j in range(w):
            count += has_crossed_mas_at(i, j, board)
    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
