from collections import defaultdict
from itertools import permutations, count
import math

def parse(text):
    """
    >>> shape, board = parse(EXAMPLE_TEXT)
    >>> shape
    (12, 12)
    >>> sorted(board.items())[:5]
    [((1, 8), '0'), ((2, 5), '0'), ((3, 7), '0'), ((4, 4), '0'), ((5, 6), 'A')]
    """
    board = {}
    for i, line in enumerate(text.strip().split('\n')):
        for j, x in enumerate(line):
            if x != '.':
                board[i, j] = x
    shape = (i + 1, j + 1)
    return shape, board

def render(shape, board, marks):
    lines = []
    m, n = shape
    for i in range(m):
        row = []
        for j in range(n):  
            if (i, j) in marks:
                row.append(marks[(i, j)])
            elif (i, j) in board:
                row.append(board[(i, j)])
            else:
                row.append('.')
        lines.append(''.join(row))
    return '\n'.join(lines)

def group_by_kind(board):
    locations_by_type = defaultdict(set)
    for ij, kind in board.items():
        locations_by_type[kind].add(ij)
    return dict(locations_by_type)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    14
    """
    shape, board = parse(text)
    m, n = shape
    locations_by_type = group_by_kind(board)
    antinodes = {}
    for kind, locations in locations_by_type.items():
        for pair in permutations(locations, 2):
            (i0, j0), (i1, j1) = pair
            di = i1 - i0
            dj = j1 - j0
            antinodes[(i1 + di, j1 + dj)] = '#'
            antinodes[(i0 - di, j0 - dj)] = '#'
    count = 0
    for i, j in antinodes:
        if 0 <= i < m and 0 <= j < n:
            count += 1
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    34
    """
    shape, board = parse(text)
    m, n = shape
    locations_by_type = group_by_kind(board)
    antinodes = {}
    for kind, locations in locations_by_type.items():
        for pair in permutations(locations, 2):
            (i0, j0), (i1, j1) = pair
            di = i1 - i0
            dj = j1 - j0
            delta = math.gcd(di, dj)
            di //= delta
            dj //= delta
            for k in count():
                i = i0 + di *k
                j = j0 + dj * k
                if 0 <= i < m and 0 <= j < n:
                    antinodes[(i, j)] = '#'
                else:
                    break
            for k in count():
                i = i0 - di * k
                j = j0 - dj * k
                if 0 <= i < m and 0 <= j < n:
                    antinodes[(i, j)] = '#'
                else:
                    break           
    return len(antinodes)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
