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
    i1, j1 = n_rows - 1, n_cols - 1
    priority_queue = []
    heappush(priority_queue, (0, 1, 0, 0, '>'))
    visited = {(0, 0, '>'): 0b1 << 1}
    # For part-2 we have to assume we start out heading east, but I can't find
    # that in description. Part-1 worked either way.
    while priority_queue:
        cost, count, i, j, heading = heappop(priority_queue)
        # If we've our finish condition, return current cost
        if i == i1 and j == j1 and count >= min_count:
            return cost
        for new_heading, new_count, di, dj in find_new_headings_info(
            heading, count, min_count, max_count
        ):
            if 0 <= (new_i := i + di) < n_rows and 0 <= (new_j := j + dj) < n_cols:
                new_cost = cost + board[new_i][new_j]
                # If we've seen this state before and it was better last time, skip
                key = (new_i, new_j, new_heading)
                new_count_bit_vector = 1 << new_count
                if key in visited:
                    visited_at_count = visited[key]
                    if visited_at_count & new_count_bit_vector:
                        # If we've seen this state before skip it
                        continue
                    # Set the current state as visited
                    visited_at_count |= new_count_bit_vector
                else:
                    # Create a new bit vector for this key and mark this state as visited
                    visited_at_count = new_count_bit_vector
                if new_count >= min_count:
                    # If new_count >= min_count, all higher counts are worse
                    # This sets all the bits at and above new_count
                    visited_at_count |= ~0 << new_count
                visited[key] = visited_at_count

                heappush(
                    priority_queue,
                    (new_cost, new_count, new_i, new_j, new_heading),
                )
    raise RuntimeError("no path found")


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
