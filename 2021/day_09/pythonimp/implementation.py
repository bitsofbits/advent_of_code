from math import inf

EXAMPLE_TEXT = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def parse(text):
    board = {}
    for i, row in enumerate(text.strip().split("\n")):
        for j, c in enumerate(row):
            board[i, j] = int(c)
    return board


def low_points(board):
    max_i = max(i for (i, j) in board)
    max_j = max(j for (i, j) in board)
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            cnt = 0
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if board[i, j] < board.get((i + di, j + dj), inf):
                    cnt += 1
            if cnt == 4:
                yield (i, j)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    15
    """
    board = parse(text)
    return sum(board[k] + 1 for k in low_points(board))


def flood_fill(start, board, maxval):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> sorted(flood_fill((0, 1), board, 8))
    [(0, 0), (0, 1), (1, 0)]
    """
    pending = [start]
    processed = set()
    while pending:
        (i, j) = k = pending.pop()
        processed.add(k)
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            k1 = (i + di, j + dj)
            if board.get(k1, inf) <= maxval and k1 not in processed:
                pending.append(k1)
    return processed


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1134
    """
    board = parse(text)
    basin_sizes = [len(flood_fill(k, board, 8)) for k in low_points(board)]
    basin_sizes.sort()
    return basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
