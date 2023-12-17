# from collections import deque
from functools import cache
from heapq import heapify, heappop, heappush

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


deltas = {'>': (0, 1), '^': (-1, 0), '<': (0, -1), 'v': (1, 0)}


def find_best_cost(board, min_count, max_count):
    n_rows = len(board)
    n_cols = len(board[0])
    start = (0, 0)
    end = (n_rows - 1, n_cols - 1)

    @cache
    def find_new_headings_info(heading, count):
        values = []
        for new_heading in next_headings[heading]:
            is_new_heading = heading != new_heading
            if is_new_heading:
                if count < min_count:
                    continue
                new_count = 1
            else:
                if count >= max_count:
                    continue
                new_count = count + 1
            di, dj = deltas[new_heading]
            values.append((new_heading, new_count, di, dj))
        return tuple(values)

    best_cost = inf
    queue = []
    heappush(queue, (0, *start, '>', 1))
    # For part-2 we have to assume we start out heading east, but I can't find
    # that in description. Part-1 worked either way.
    # heappush(queue, (inf, *start, 'v', 1, 0))
    seen = {}
    max_possible_cost = 9 * sum(end)
    max_count_plus_one = max_count + 1
    while queue:
        cost, i, j, heading, count = heappop(queue)

        key = (i, j, heading)
        if key in seen:
            prev_costs = seen[key]
            if cost >= prev_costs[count]:
                continue
            if min_count <= 1 and cost >= min(prev_costs[:count]):
                continue
        else:
            seen[key] = [max_possible_cost] * max_count_plus_one
        seen[key][count] = cost
        if cost >= best_cost:
            continue
        if (i, j) == end and count >= min_count:
            best_cost = cost
            continue
        for new_heading, new_count, di, dj in find_new_headings_info(heading, count):
            new_i = i + di
            new_j = j + dj
            if 0 <= new_i < n_rows and 0 <= new_j < n_cols:
                new_cost = cost + board[new_i][new_j]
                if new_cost < best_cost:
                    heappush(
                        queue,
                        (new_cost, new_i, new_j, new_heading, new_count),
                    )
    return best_cost


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    102
    """
    board = parse(text)
    return find_best_cost(board, min_count=1, max_count=3)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    94

    >>> part_2(EXAMPLE2_TEXT)
    71

    # 1177 is too low
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
