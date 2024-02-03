# from heapq import heappop, heappush


def parse_coord(text):
    if '..' in text:
        a, b = (int(x) for x in text.split('..'))
        return list(range(a, b + 1))
    else:
        return [int(text)]


def parse_line(line):
    x, y = line.strip().split(', ')
    if not x.startswith('x'):
        x, y = y, x
    assert x.startswith('x=')
    assert y.startswith('y=')
    x = parse_coord(x[2:])
    y = parse_coord(y[2:])
    if len(x) > len(y):
        y = y * len(x)
    else:
        x = x * len(y)
    assert len(x) == len(y)
    return x, y


def render(board, filled=(), stationary=()):
    i0 = min(i for ((i, j)) in board)
    i1 = max(i for ((i, j)) in board) + 1
    j0 = min(j for ((i, j)) in board)
    j1 = max(j for ((i, j)) in board) + 1
    rows = []
    for i in range(i0 - 1, i1 + 1):
        row = []
        for j in range(j0 - 1, j1 + 1):
            key = (i, j)
            if key in board:
                row.append('#')
            elif key == (0, 500):
                row.append('+')
            elif key in stationary:
                row.append('~')
            elif key in filled:
                row.append('|')
            else:
                row.append('•')
        rows.append(''.join(row))
    return '\n'.join(rows)


def parse(text):
    """
    >>> print(render(parse(EXAMPLE_TEXT)))
    ••••••+•••••••
    ••••••••••••#•
    •#••#•••••••#•
    •#••#••#••••••
    •#••#••#••••••
    •#•••••#••••••
    •#•••••#••••••
    •#######••••••
    ••••••••••••••
    ••••••••••••••
    ••••#•••••#•••
    ••••#•••••#•••
    ••••#•••••#•••
    ••••#######•••
    ••••••••••••••
    >>> _ = parse(INPUT_TEXT)
    """
    lines = [parse_line(x) for x in text.strip().split('\n')]
    board = set()
    for line in lines:
        for x, y in zip(*line):
            board.add((y, x))
    return frozenset(board)


def is_stationary(i0, j0, stationary, min_j, max_j):
    for j in reversed(range(min_j - 100, j0 + 1)):
        if (i0 + 1, j) not in stationary:
            return False
        if (i0, j) in stationary:
            break
    else:
        raise RuntimeError()
    for j in range(j0, max_j + 100):
        if (i0 + 1, j) not in stationary:
            return False
        if (i0, j) in stationary:
            break
    else:
        raise RuntimeError()
    return True


def downward_flood_fill(board, start):
    stationary = set(board)
    bottom = max(i for (i, j) in board)
    changed = True
    min_j = min(j for (i, j) in board)
    max_j = max(j for (i, j) in board)

    while changed:
        # print(len(stationary))
        queue = [start]
        occupied = set(stationary)
        changed = False
        while queue:
            # print(queue)
            i0, j0 = key = queue.pop()
            if key in occupied:
                continue
            occupied.add(key)
            below = (i0 + 1, j0)
            left = (i0, j0 - 1)
            right = (i0, j0 + 1)
            if is_stationary(i0, j0, stationary, min_j, max_j):
                stationary.add(key)
                changed = True
            if below in stationary:
                left = (i0, j0 - 1)
                right = (i0, j0 + 1)
                for next_key in [left, right]:
                    if next_key not in occupied:
                        queue.append(next_key)
            else:
                if below[0] <= bottom:
                    queue.append(below)
        # Add in
    return occupied - board, stationary


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    ••••••+•••••••
    ••••••|•••••#•
    •#••#||||•••#•
    •#••#~~#|•••••
    •#••#~~#|•••••
    •#~~~~~#|•••••
    •#~~~~~#|•••••
    •#######|•••••
    ••••••••|•••••
    •••|||||||||••
    •••|#~~~~~#|••
    •••|#~~~~~#|••
    •••|#~~~~~#|••
    •••|#######|••
    ••••••••••••••
    57

    50838
    """
    board = parse(text)
    filled, stationary = downward_flood_fill(board, (0, 500))
    print(render(board, filled, stationary))
    i0 = min(i for (i, j) in board)
    i1 = max(i for (i, j) in board) + 1
    return sum(i0 <= i <= i1 for (i, j) in filled)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    29
    """
    board = parse(text)
    filled, stationary = downward_flood_fill(board, (0, 500))
    return len(stationary - board)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    doctest.testmod()
