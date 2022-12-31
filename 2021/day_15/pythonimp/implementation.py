from heapq import heappop, heappush

EXAMPLE_TEXT = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""


def parse(text):
    """
    >>> board = parse(EXAMPLE_TEXT)
    >>> list(board.items())[:4]
    [((0, 0), 1), ((0, 1), 1), ((0, 2), 6), ((0, 3), 3)]
    """
    board = {}
    for i, line in enumerate(text.strip().split("\n")):
        for j, c in enumerate(line):
            board[i, j] = int(c)
    return board


def traverse(board):
    H = max(i for (i, j) in board) + 1
    W = max(j for (i, j) in board) + 1
    N = H * W

    B = [board[i, j] for i in range(H) for j in range(W)]

    max_dist = (H - 1) + (W - 1)
    scores = [9 * max_dist] * N
    heap = [(max_dist, 0, 0)]
    while heap:
        score, i0, j0 = heappop(heap)
        for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if 0 <= (i := i0 + di) < H and 0 <= (j := j0 + dj) < W:
                k = i * W + j
                next_score = score + B[k] - di - dj
                if next_score < scores[k]:
                    scores[k] = next_score
                    heappush(heap, (next_score, i, j))

    return scores[N - 1]


def build_big_board(board, n):
    di = max(i for (i, j) in board) + 1
    dj = max(j for (i, j) in board) + 1
    big_board = {}
    for a in range(n):
        for b in range(n):
            for k, c in board.items():
                i, j = k
                c = (c + a + b - 1) % 9 + 1
                big_board[i + a * di, j + b * dj] = c
    return big_board


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    40
    """
    board = parse(text)
    return traverse(board)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    315
    """
    small_board = parse(text)
    board = build_big_board(small_board, 5)
    return traverse(board)

    # 3688 too high


if __name__ == "__main__":
    import doctest

    doctest.testmod()
