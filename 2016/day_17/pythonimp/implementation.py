from hashlib import md5
from heapq import heappop, heappush
from math import inf


def open_doors(seed, path):
    """
    >>> open_doors(EXAMPLE_TEXT, "")
    ['U', 'D', 'L']
    >>>
    >>> open_doors(EXAMPLE_TEXT, "D")
    ['U', 'L', 'R']
    >>> open_doors(EXAMPLE_TEXT, "DR")
    []
    >>> open_doors(EXAMPLE_TEXT, "DU")
    ['R']
    """
    digest = md5(f"{seed}{path}".encode("ascii")).hexdigest()
    return [door for (door, x) in zip("UDLR", digest) if x in "bcdef"]


def traverse(seed):
    """
    >>> traverse("ihgpwlah")
    'DDRRRD'
    >>> traverse("kglvqrro")
    'DDUDRLRRUDRD'
    >>> traverse("ulqzkmiv")
    'DRURDRUDDLLDLUURRDULRLDUUDDDRR'
    """
    queue = [(6, 0, 0, 0, "")]
    lowest_cnt = inf
    shortest_path = None
    while queue:
        _, cnt, row, col, path = heappop(queue)
        if (row, col) == (3, 3):
            if cnt < lowest_cnt:
                shortest_path = path
                lowest_cnt = cnt
            continue
        for door in open_doors(seed, path):
            next_row = row
            next_col = col
            match door:
                case "U":
                    next_row -= 1
                case "D":
                    next_row += 1
                case "L":
                    next_col -= 1
                case "R":
                    next_col += 1
                case _:
                    raise ValueError(door)
            if not ((0 <= next_row < 4) and (0 <= next_col < 4)):
                continue
            next_path = path + door
            next_cnt = len(next_path)
            next_estimate = (3 - next_row) + (3 - next_col) + next_cnt
            if next_estimate >= lowest_cnt:
                continue
            heappush(queue, (next_estimate, next_cnt, next_row, next_col, next_path))
    return shortest_path


# 10 is not right


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    'hijkl'
    """
    return text.strip()


def part_1(text):
    """
    >>> part_1('ihgpwlah')
    'DDRRRD'
    """
    return traverse(parse(text))


def traverse_longest(seed):
    """
    >>> traverse_longest("ihgpwlah")
    370
    >>> traverse_longest("kglvqrro")
    492
    >>> traverse_longest("ulqzkmiv")
    830
    """
    queue = [(0, 0, 0, "")]
    largest_cnt = 0
    while queue:
        cnt, row, col, path = heappop(queue)
        if (row, col) == (3, 3):
            largest_cnt = max(largest_cnt, cnt)
            continue
        for door in open_doors(seed, path):
            next_row = row
            next_col = col
            match door:
                case "U":
                    next_row -= 1
                case "D":
                    next_row += 1
                case "L":
                    next_col -= 1
                case "R":
                    next_col += 1
                case _:
                    raise ValueError(door)
            if not ((0 <= next_row < 4) and (0 <= next_col < 4)):
                continue
            next_path = path + door
            next_cnt = len(next_path)
            heappush(queue, (next_cnt, next_row, next_col, next_path))
    return largest_cnt


def part_2(text):
    """
    >>> part_2("ihgpwlah")
    370
    """
    return traverse_longest(parse(text))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
