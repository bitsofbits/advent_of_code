from heapq import heappop, heappush
from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:3]
    [(4, 5), (2, 4), (5, 4)]
    """
    coords = []
    for row in text.strip().split("\n"):
        x, y = (int(x) for x in row.split(","))
        coords.append((y, x))
    return coords


def render(board):
    min_i = min(i for (i, j) in board)
    min_j = min(j for (i, j) in board)
    max_i = max(i for (i, j) in board)
    max_j = max(j for (i, j) in board)

    rows = []
    for i in range(min_i, max_i + 1):
        row = []
        for j in range(min_j, max_j + 1):
            if (i, j) in board:
                row.append("#")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def create_board(coords, size):
    """
    >>> coords = parse(EXAMPLE_TEXT)
    >>> board = create_board(coords[:12], 7)
    >>> print(render(board))
    #########
    #...#...#
    #..#..#.#
    #....#..#
    #...#..##
    #..#..#.#
    #.#..#..#
    ##.#....#
    #########
    """
    board = {xy for xy in coords}
    for i in range(-1, size + 1):
        board.add((i, -1))
        board.add((i, size))
        board.add((-1, i))
        board.add((size, i))
    return board


def find_path(board, start, end):
    queue = [(0, start, ())]
    seen = set()
    while queue:
        steps, location, path = heappop(queue)
        path += (location,)
        if location == end:
            return path
        if location in seen:
            continue
        seen.add(location)
        i, j = location
        next_steps = steps + 1
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_location = (i + di, j + dj)
            if next_location not in board:
                heappush(queue, (next_steps, next_location, path))


def part_1(text, size=71, steps=1024):
    """
    >>> part_1(EXAMPLE_TEXT, size=7, steps=12)
    22
    """
    coords = parse(text)
    board = create_board(coords[:steps], size)
    return len(find_path(board, (0, 0), (size - 1, size - 1))) - 1


# def find_all_paths(board, start, end):
#     queue = [(0, start, ())]
#     seen = set()
#     while queue:
#         steps, location, path = heappop(queue)
#         path += (location,)
#         if location == end:
#             yield path
#         key = frozenset(path)
#         if key in seen:
#             continue
#         seen.add(key)
#         i, j = location
#         next_steps = steps + 1
#         for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             next_location = (i + di, j + dj)
#             if next_location not in board:
#                 heappush(queue, (next_steps, next_location, path))


def part_2(text, size=71, initial_steps=1024):
    """
    >>> print(part_2(EXAMPLE_TEXT, size=7, initial_steps=12))
    6,1
    """
    coords = parse(text)
    start = (0, 0)
    end = (size - 1, size - 1)
    board = create_board(coords[:initial_steps], size)
    path = find_path(board, start, end)
    for location in coords[initial_steps:]:
        board.add(location)
        if location in path:
            path = find_path(board, start, end)
            if path is None:
                i, j = location
                return f"{j},{i}"


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
