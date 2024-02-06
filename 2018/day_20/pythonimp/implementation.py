from collections import defaultdict
from math import inf


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    '^ENWWW(NEEE|SSE(EE|N))$'
    """
    return text.strip()


deltas = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}


def build_board_from_pattern(pattern):
    assert pattern.startswith('^') and pattern.endswith('$')
    pattern = pattern[1:-1]
    i0 = j0 = 0
    board = set([(i0, j0)])
    shortest_path_to = defaultdict(lambda: inf)
    shortest_path_to[i0, j0] = 0
    stack = [(0, 0, 0, 0)]
    pattern_length = len(pattern)
    #
    while stack:
        start_index, i, j, count = stack.pop()
        index = start_index
        while index < pattern_length:
            x = pattern[index]
            if x == '|':
                _, i, j, count = stack[-1]
            elif x == '(':
                stack.append((index, i, j, count))
            elif x == ')':
                stack.pop()
            else:
                di, dj = deltas[x]
                i += di
                j += dj
                count += 1
                key = (i, j)
                board.add(key)
                shortest_path_to[key] = min(shortest_path_to[key], count)
            index += 1
    return board, shortest_path_to


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    10
    >>> part_1('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')
    23
    >>> part_1('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')
    31
    """
    pattern = parse(text)
    board, shortest_path_to = build_board_from_pattern(pattern)
    return max(shortest_path_to.values())


def part_2(text):
    pattern = parse(text)
    board, shortest_path_to = build_board_from_pattern(pattern)
    return sum(x >= 1000 for x in shortest_path_to.values())


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
