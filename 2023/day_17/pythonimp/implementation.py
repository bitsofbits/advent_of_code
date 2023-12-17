from collections import deque
from functools import cache

from numpy import inf


def render(board):
    lines = []
    for row in board:
        lines.append(''.join(str(x) for x in row))
    return '\n'.join(lines)


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)[:4]))
    2413432311323
    3215453535623
    3255245654254
    3446585845452
    """
    board = []
    for line in text.strip().split():
        row = []
        for x in line:
            row.append(int(x))
        board.append(row)
    return board


# Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

next_headings = {'>': '^>v', '^': '<^>', '<': 'v<^', 'v': '>v<'}


@cache
def find_new_headings(heading, count):
    new_headings = next_headings[heading]
    new_headings = [(x, 1 if (x != heading) else count + 1) for x in new_headings]
    return new_headings


deltas = {'>': (0, 1), '^': (-1, 0), '<': (0, -1), 'v': (1, 0)}


def find_best_cost(board, min_count=0, max_count=3):
    n_rows = len(board)
    n_cols = len(board[0])
    end = (n_rows - 1, n_cols - 1)
    start = (0, 0)
    best_cost = inf
    queue = deque([(*start, '>', 0, 0), (*start, 'v', 0, 0)])
    seen = {}
    while queue:
        i0, j0, last_heading, count, cost = queue.popleft()
        if cost >= best_cost:
            continue
        if (i0, j0) == end and count >= min_count:
            best_cost = min(best_cost, cost)
            continue
        key = (i0, j0, last_heading)
        if key in seen:
            prev_costs = seen[key]
            target_cost = min(prev_costs[:count])
            if cost >= target_cost:
                continue
        else:
            seen[key] = [inf] * max_count
        seen[key][count - 1] = cost
        for heading, new_count in find_new_headings(last_heading, count):
            if new_count > max_count:
                continue
            if new_count == 1 and 1 <= count <= min_count:
                assert heading != last_heading, (
                    heading,
                    last_heading,
                    new_count,
                    count,
                )
                # print(new_count, count)
                continue
            di, dj = deltas[heading]
            i = i0 + di
            j = j0 + dj
            if 0 <= i < n_rows and 0 <= j < n_cols:
                queue.append((i, j, heading, new_count, cost + board[i][j]))
    return best_cost


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    102
    """
    board = parse(text)
    return find_best_cost(board, min_count=0, max_count=3)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    94

    >>> part_2(EXAMPLE2_TEXT)
    71
    """
    board = parse(text)
    return find_best_cost(board, min_count=4, max_count=10)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
