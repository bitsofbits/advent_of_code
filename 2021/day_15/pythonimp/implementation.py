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


def traverse(board):
    start = (0, 0)
    end = (max(i for (i, j) in board), max(j for (i, j) in board))

    def optimistic_score(x):
        s, (i, j), *_ = x
        return s + (end[0] - i) + (end[1] - j)

    def pessimistic_score(x):
        s, (i, j), *_ = x
        return s + 9 * (end[0] - i) + 9 * (end[1] - j)

    stack = [(0, start, set())]
    scores = {}
    best_score = inf
    while stack:
        stack.sort(key=optimistic_score)
        score, (i, j), visited = stack.pop()
        for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            k1 = i + di, j + dj
            if k1 in board and k1 not in visited:
                next_score = score + board[k1]
                good_score = optimistic_score((next_score, k1))
                if good_score < best_score and score < scores.get(k1, inf):
                    scores[k1] = score
                    bad_score = pessimistic_score((next_score, k1))
                    best_score = min(best_score, bad_score)
                    if k1 != end:
                        stack.append((next_score, k1, visited | {k1}))
                    else:
                        print(next_score)
    return best_score


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
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod()
