from collections import deque
from functools import cache
from math import inf

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


# class ScoreEstimator:
#     """
#     >>> board = parse(EXAMPLE_TEXT)
#     >>> scorer = ScoreEstimator(board)
#     >>> scorer.pessimistic(9, 9)
#     0
#     >>> scorer.pessimistic(0, 0)
#     """

#     def __init__(self, board):
#         self.board = board
#         self.end = (max(i for (i, j) in board), max(j for (i, j) in board))

#     @cache
#     def pessimistic(self, i, j):
#         score = 0
#         i1, j1 = self.end
#         while (i, j) != self.end:
#             di, dj = (i1 - i), (j1 - j)
#             if di > dj:
#                 i += 1
#             else:
#                 j += 1
#             if (i)
#             score += self.board[i, j]
#         return score


def traverse(board):
    start = (0, 0)
    end = (max(i for (i, j) in board), max(j for (i, j) in board))

    # scorer = ScoreEstimator(board)

    def optimistic_score(s, i, j):
        return s + ((end[0] - i) + (end[1] - j))

    def pessimistic_score(s, i, j):
        return s + 9 * ((end[0] - i) + (end[1] - j))

    stack = [(sum(end), 0, start, set())]
    scores = {}
    best_score = 9 * sum(end)

    assert end[0] == end[1]

    while stack:
        stack.sort(reverse=True)
        _, score, (i, j), visited = stack.pop()
        for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            k1 = i + di, j + dj
            if k1 in board and k1 not in visited:
                next_score = score + board[k1]
                if next_score < scores.get(k1, inf):
                    scores[k1] = next_score
                    good_score = optimistic_score(next_score, *k1)
                    if good_score < best_score:
                        best_score = min(best_score, pessimistic_score(next_score, *k1))
                        if k1 != end:
                            stack.append((good_score, next_score, k1, visited | {k1}))
    return best_score


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
