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


next_headings = {'>': '^>v', '^': '<^>', '<': 'v<^', 'v': '>v<'}
deltas = {'>': (0, 1), '^': (-1, 0), '<': (0, -1), 'v': (1, 0)}


@cache
def find_new_headings_info(heading, count, min_count, max_count):
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


def find_best_cost(board, min_count, max_count):
    n_rows = len(board)
    n_cols = len(board[0])
    i0, j0 = (0, 0)
    i1, j1 = (n_rows - 1, n_cols - 1)
    max_possible_cost = 9 * (i1 + j1)
    best_cost = max_possible_cost
    queue = []
    heappush(queue, (0, 1, i0, j0, '>'))
    # For part-2 we have to assume we start out heading east, but I can't find
    # that in description. Part-1 worked either way.
    # heappush(queue, (0, i0, j0, 'v', 1))
    max_count_plus_one = max_count + 1
    state_to_costs = {}
    while queue:
        cost, count, i, j, heading = heappop(queue)
        # If this is already worse than our current best cost, quit
        if cost >= best_cost:
            continue
        # If we've our finish condition, record best cost and quit
        if i == i1 and j == j1 and count >= min_count:
            best_cost = cost
            continue
        for new_heading, new_count, di, dj in find_new_headings_info(
            heading, count, min_count, max_count
        ):
            if 0 <= (new_i := i + di) < n_rows and 0 <= (new_j := j + dj) < n_cols:
                new_cost = cost + board[new_i][new_j]
                # If we've seen this state before and it was better last time, quit
                key = (new_i, new_j, new_heading)
                if key in state_to_costs:
                    costs = state_to_costs[key]
                    if new_cost >= costs[new_count]:
                        continue
                    if min_count <= 1:
                        # Lower counts are always better for part 1 -- exploiting this
                        # doubles the speed but doesn't work for 2 since lower counts
                        # may not be better there.
                        if new_cost >= min(costs[:new_count]):
                            continue
                else:
                    state_to_costs[key] = [max_possible_cost] * max_count_plus_one
                state_to_costs[key][new_count] = new_cost
                #
                heappush(
                    queue,
                    (new_cost, new_count, new_i, new_j, new_heading),
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
