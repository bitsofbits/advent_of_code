from functools import cache
from heapq import heappop, heappush
from math import inf

TARGET_BOARD = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #########  \
"""


COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def parse(text):
    """ """
    walls = set()
    amphs = {}
    hall = set()
    for i, line in enumerate(text.strip().split("\n")):
        for j, c in enumerate(line):
            if c == "#":
                walls.add((i, j))
            elif c in "ABCD":
                amphs[i, j] = c
            elif c == ".":
                hall.add((i, j))
    return walls, amphs, hall


class Board:
    """
    >>> board = Board.from_text(EXAMPLE_TEXT)
    >>> board.amphs   # doctest: +ELLIPSIS
    {(2, 3): 'B', (2, 5): 'C', (2, 7): 'B', (2, 9): 'D', (3, 3): 'A', (3, 5): 'D', ...
    >>> board
    |#############|
    |#...........#|
    |###B#C#B#D###|
    |  #A#D#C#A#  |
    |  #########  |
    >>> len(board.hall_dests), len(board.rooms)
    """

    walls, target_amphs, hall = parse(TARGET_BOARD)
    hall_dests = hall - {(1, 3), (1, 5), (1, 7), (1, 9)}
    amph_homes = {k: set() for k in "ABCD"}
    rooms = set(target_amphs)
    for loc, a in target_amphs.items():
        amph_homes[a].add(loc)
    amph_home_j = {}
    for a, homes in amph_homes.items():
        for (i, j) in homes:
            assert j == amph_home_j.get(a, j) == j
            amph_home_j[a] = j

    del loc, homes, a, j

    def __init__(self, walls, amphs, hall):
        self.walls = walls
        self.initial_amphs = amphs.copy()
        self.amphs = amphs
        self.hall = hall

    @classmethod
    def from_text(cls, text):
        walls, amphs, hall = parse(text)
        return cls(walls, amphs, hall)

    def __repr__(self):
        max_i = max(i for (i, j) in self.walls)
        max_j = max(j for (i, j) in self.walls)
        text = ""
        for i in range(max_i + 1):
            text += "|"
            for j in range(max_j + 1):
                if (i, j) in self.amphs:
                    text += self.amphs[i, j]
                elif (i, j) in self.walls:
                    text += "#"
                elif (i, j) in self.hall:
                    text += "."
                elif (i, j) in self.initial_amphs:
                    text += "."
                else:
                    text += " "
            text += "|\n"
        return text[:-1]

    @classmethod
    def estimate_remaining_cost(cls, amphs):
        """
        >>> board = Board.from_text(EXAMPLE_TEXT)
        >>> amphs = frozenset(board.amphs.items())
        >>> board.estimate_remaining_cost(amphs)
        7489
        >>> board = Board.from_text(TARGET_BOARD)
        >>> amphs = frozenset(board.amphs.items())
        >>> board.estimate_remaining_cost(amphs)
        0
        """
        cost = 0
        for (i, j), kind in amphs:
            target_j = cls.amph_home_j[kind]
            dj = abs(j - target_j)
            cost += COSTS[kind] * (dj + (dj > 0) * i)  # Really (i - 1 + 1)
        return cost

    @classmethod
    def find_path(cls, start, end):
        """
        >>> board = Board.from_text(EXAMPLE_TEXT)

        """
        i1, j1 = start
        i2, j2 = end
        i, j = i1, j1
        steps = set()

        # Walk into the hall
        if start in cls.rooms:
            for i in range(i1 - 1, i2 - 1, -1):
                steps.add((i, j))
            assert i == i2

        # Walk down the hall
        dj = (j2 > j1) - (j1 > j2)
        for j in range(j1 + dj, j2 + dj, dj):
            steps.add((i, j))
        assert j == j2

        # Walk into a rooms
        if end in cls.rooms:
            for i in range(i + 1, i2 + 1):
                steps.add((i, j))
        return steps

    @classmethod
    def send_amphs_home(cls, amphs):
        """
        >>> board = Board.from_text(EXAMPLE_TEXT)

        # >>> board.send_amphs_home(board.amphs)
        # 12521
        """
        paths = {}
        for start in cls.hall_dests:
            for end in cls.rooms:
                paths[start, end] = cls.find_path(start, end)
        for start in cls.rooms:
            for end in cls.hall_dests:
                paths[start, end] = cls.find_path(start, end)

        visitor_mask = {}
        for kind, locs in cls.amph_homes.items():
            visitor_mask[kind] = set()
            for other_kind in "ABCD":
                if kind != other_kind:
                    for loc in locs:
                        visitor_mask[kind].add((loc, other_kind))
        cls.visitor_mask = visitor_mask

        print("A")

        cls.path_map = paths

        amphs = frozenset(amphs.items())
        estimated = cls.estimate_remaining_cost(amphs)
        opendests = frozenset(cls.hall)  # opecells

        queue = [(estimated, 0, amphs, opendests)]
        best_score = inf
        score_by_state = {}
        target = frozenset(cls.target_amphs.items())
        while queue:
            _, score, amphs, opendests = heappop(queue)
            for start, kind in amphs:
                for end, count in cls.find_valid_moves(start, kind, amphs, opendests):
                    new_score = score + count * COSTS[kind]
                    if new_score >= best_score:
                        continue
                    new_amphs = amphs ^ {(start, kind), (end, kind)}
                    new_opendests = opendests ^ {start, end}
                    if new_amphs == target:
                        best_score = min(best_score, new_score)
                    else:
                        estimated = new_score + cls.estimate_remaining_cost(new_amphs)
                        if estimated < score_by_state.get(new_amphs, inf):
                            score_by_state[new_amphs] = estimated
                            heappush(
                                queue,
                                (
                                    estimated,
                                    new_score,
                                    new_amphs,
                                    new_opendests,
                                    # new_home_counts,
                                ),
                            )
        return best_score

    @classmethod
    def find_valid_moves(cls, start, kind, amphs, opendests):
        if start in cls.hall_dests:
            if amphs & cls.visitor_mask[kind]:
                return
            ends = cls.amph_homes[kind] & opendests
        else:
            ends = cls.hall_dests & opendests
        for end in ends:
            path = cls.path_map[start, end]
            if len(path & opendests) == len(path):  # TODO: need filled_dests?
                yield end, len(path)
            # # count = cls.valid_move_count(start, end, opendests)
            # if count > 0:
            #     yield (end, count)

    # @classmethod
    # def valid_move_count(cls, start, end, opendests):
    #     """
    #     >>> board = Board.from_text(EXAMPLE_TEXT)

    #     """
    #     i1, j1 = start
    #     i2, j2 = end
    #     cnt = 0
    #     i, j = i1, j1
    #     if start in cls.rooms:
    #         # Walk into the hall
    #         for i in range(i1 - 1, i2 - 1, -1):
    #             cnt += 1
    #             if (i, j) not in opendests:
    #                 return 0
    #         assert i == i2

    #     # Walk down the hall
    #     dj = (j2 > j1) - (j1 > j2)
    #     for j in range(j1 + dj, j2 + dj, dj):
    #         cnt += 1
    #         if (i, j) not in opendests:
    #             return 0
    #     assert j == j2

    #     if end in cls.rooms:
    #         for i in range(i + 1, i2 + 1):
    #             cnt += 1
    #             if (i, j) not in opendests:
    #                 return 0

    #     return cnt


def part_1(text):
    """
    # >>> part_1(EXAMPLE_TEXT)
    12521
    """
    board = Board.from_text(text)
    return board.send_amphs_home(board.amphs)


def augment_text(text):
    """
    >>> print(augment_text(EXAMPLE_TEXT))
    #############
    #...........#
    ###B#C#B#D###
      #D#C#B#A#
      #D#B#A#C#
      #A#D#C#A#
      #########
    >>> board = Board.from_text(augment_text(EXAMPLE_TEXT))
    >>> board
    |#############|
    |#...........#|
    |###B#C#B#D###|
    |  #D#C#B#A#  |
    |  #D#B#A#C#  |
    |  #A#D#C#A#  |
    |  #########  |

    """
    lines = text.strip().split("\n")
    return "\n".join(lines[:3] + ["  #D#C#B#A#", "  #D#B#A#C#"] + lines[3:])


TARGET_BOARD2 = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########\
"""


class Board2(Board):
    """
    >>> board = Board2.from_text(EXAMPLE_TEXT)
    >>> board
    |#############|
    |#...........#|
    |###B#C#B#D###|
    |  #D#C#B#A#  |
    |  #D#B#A#C#  |
    |  #A#D#C#A#  |
    |  #########  |
    """

    walls, target_amphs, hall = parse(TARGET_BOARD2)
    hall_dests = hall - {(1, 3), (1, 5), (1, 7), (1, 9)}
    amph_homes = {k: set() for k in "ABCD"}
    rooms = set(target_amphs)
    for loc, a in target_amphs.items():
        amph_homes[a].add(loc)
    amph_home_j = {}
    for a, homes in amph_homes.items():
        for (i, j) in homes:
            assert j == amph_home_j.get(a, j) == j
            amph_home_j[a] = j
    del loc, homes, a, j

    @classmethod
    def from_text(cls, text):
        walls, amphs, hall = parse(augment_text(text))
        return cls(walls, amphs, hall)


def part_2(text):
    """
    # >>> part_2(EXAMPLE_TEXT)
    44169
    """
    board = Board2.from_text(text)
    return board.send_amphs_home(board.amphs)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
