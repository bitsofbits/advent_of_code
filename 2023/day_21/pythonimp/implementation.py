from copy import deepcopy
from functools import cache
from heapq import heappop, heappush


def sign(x):
    return int(x > 0) - int(x < 0)


def parse(text):
    """
    >>> board, height, width, start = parse(EXAMPLE_TEXT)
    >>> start
    (5, 5)
    """
    board = []
    start = None
    lines = text.strip().split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        board.append(list(line))
        if 'S' in line:
            start = (i, line.index('S'))
    height = len(lines)
    width = len(line)
    return board, height, width, start


def possible_visits(board, height, width, start, steps):
    queue = []
    heappush(queue, (0, *start))
    seen = deepcopy(board)
    seen[start[0]][start[1]] = 0
    while queue:
        count, i, j = heappop(queue)
        if count < steps:
            next_count = count + 1
            for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                i0 = i + di
                j0 = j + dj
                if 0 <= i0 < height and 0 <= j0 < width and seen[i0][j0] == '.':
                    seen[i0][j0] = next_count
                    heappush(queue, (next_count, i0, j0))
    return sum(
        1 for line in seen for x in line if isinstance(x, int) and x % 2 == steps % 2
    )


def part_1(text, steps=64):
    """
    >>> part_1(EXAMPLE_TEXT, steps=6)
    16

    >>> part_1(EXAMPLE_TEXT, steps=64)
    42
    """
    board, height, width, start = parse(text)
    return possible_visits(board, height, width, start, steps)


def possible_visits_2_naive(board, height, width, start, steps, parity=None):
    queue = []
    heappush(queue, (0, *start))
    seen = {}
    seen[start] = 0
    while queue:
        count, i, j = heappop(queue)
        if count < steps:
            next_count = count + 1
            for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                i0 = i + di
                j0 = j + dj
                if (i0, j0) not in seen and board[i0 % height][j0 % width] != '#':
                    seen[(i0, j0)] = next_count
                    heappush(queue, (next_count, i0, j0))
    if parity is None:
        parity = steps % 2
    # print(steps, start, parity)
    return set(k for (k, v) in seen.items() if v % 2 == parity)


def check_board(board, height, width, start):
    assert height == width
    for i in range(height):
        if board[i][start[1]] == '#':
            raise ValueError()
        if board[start[0]][i] == '#':
            raise ValueError()


def part_2(text, steps=26501365, check=False, use_simple=False):
    """

    >>> assert 1 == True
    >>> assert 0 == False

    Check that baseline application works by using on known answers
    >>> part_2(EXAMPLE_TEXT, 0, use_simple=True)
    1
    >>> part_2(EXAMPLE_TEXT, 1, use_simple=True)
    2
    >>> part_2(EXAMPLE_TEXT, 2, use_simple=True)
    4
    >>> part_2(EXAMPLE_TEXT, 50, use_simple=True)
    1594
    >>> part_2(EXAMPLE_TEXT, 100, use_simple=True)
    6536

    # >>> part_2(EXAMPLE_TEXT, 500, use_simple=True)
    # 167004
    # >>> part_2(EXAMPLE_TEXT, 1000, use_simple=True)
    # 668697

    Check that our answer aggrees with baseline for inputs
    (We can't test on example, because example doeesn't have
    corridor to edge)
    # >>> part_2(INPUT_TEXT, 460, check=True)
    # 193425

    >>> part_2(INPUT_TEXT, 11, check=True)
    137
    >>> part_2(INPUT_TEXT, 3 * 55, check=True)
    25011
    >>> part_2(INPUT_TEXT, 5 * 55, check=True)
    69268


    >>> part_2(INPUT_TEXT, 230, check=True)
    48597
    >>> part_2(INPUT_TEXT, 235, check=True)
    50748

    And yet, our final answer is wrong :-()
    >>> part_2(INPUT_TEXT, 26501365)
    638192183371494

    638192165569450 is too low :-()
    638192183371494 is wrong after fixing padding

    638192138461059 is wrong bad parity fix
    """
    board, height, width, start = parse(text)
    assert height == width
    size = height
    parity = steps % 2
    # print("steps_past_edge =", steps_past_edge)

    # Input maps has straight shots horizonally and vertically
    # So can enter at center and corners of boundaries.
    # Compute the eight cases

    if use_simple:
        return len(possible_visits_2_naive(board, size, size, start, steps))

    check_board(board, height, width, start)

    interior_steps = steps // size

    interior_reachable = sum(
        (i + j) % 2 == parity and board[i][j] != '#'
        for i in range(size)
        for j in range(size)
    )

    @cache
    def get_count(remaining_steps, entry):
        # print(remaining_steps, entry)
        # if remaining_steps > 2 * size:
        #     return interior_reachable
        local_parity = bool(parity)
        if remaining_steps % 2 != steps % 2:
            local_parity = not local_parity
        seen = possible_visits_2_naive(
            board, size, size, entry, remaining_steps, local_parity
        )
        return sum(1 for (i, j) in seen if 0 <= i < size and 0 <= j < size)

    boundary_size = 6

    if interior_steps - boundary_size > 0:
        total = (
            1 + sum(4 * i for i in range(max(interior_steps - boundary_size, 0)))
        ) * interior_reachable
    else:
        total = 0
    for abs_n in range(0, interior_steps + boundary_size):
        di = (abs_n - 1) * size + size // 2 + 1 if (abs_n > 0) else 0
        for abs_m in range(
            max(interior_steps - boundary_size - abs_n, 0),
            max(interior_steps + boundary_size - abs_n + 1, 0),
        ):
            dj = (abs_m - 1) * size + size // 2 + 1 if (abs_m > 0) else 0

            distance = di + dj
            if distance >= steps:
                continue

            signed_nm = set(
                [(abs_n, abs_m), (abs_n, -abs_m), (-abs_n, abs_m), (-abs_n, -abs_m)]
            )

            remaining_steps = steps - distance
            if remaining_steps > 5 * size:
                total += interior_reachable * len(signed_nm)
                continue

            for n, m in signed_nm:
                a = size // 2 + sign(n) * di
                b = size // 2 + sign(m) * dj

                normalized_entry = (a % size, b % size)
                total += get_count(remaining_steps, normalized_entry)

    if check:
        expected = len(possible_visits_2_naive(board, size, size, start, steps))
        assert expected == total, (
            expected,
            total,
            expected - total,
        )

    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    doctest.testmod()
