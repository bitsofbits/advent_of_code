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
    """

    target_board = TARGET_BOARD

    def __init__(self, walls, amphs, hall):
        self.walls = walls
        self.initial_amphs = amphs.copy()
        self.amphs = amphs
        self.hall = hall
        # Initialize endpoints using target board
        (_, self.target_amphs, _) = parse(self.target_board)
        self.hall_dests = hall - {(1, 3), (1, 5), (1, 7), (1, 9)}
        self.amph_homes = {k: set() for k in "ABCD"}
        self.rooms = set(self.target_amphs)
        for loc, a in self.target_amphs.items():
            self.amph_homes[a].add(loc)
        self.amph_home_j = {}
        for a, homes in self.amph_homes.items():
            for (i, j) in homes:
                assert j == self.amph_home_j.get(a, j) == j
                self.amph_home_j[a] = j
        self.amphs_per_type = len(self.rooms) // 4

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

    def find_path(self, start, end):
        """
        >>> board = Board.from_text(EXAMPLE_TEXT)

        """
        i1, j1 = start
        i2, j2 = end
        i, j = i1, j1
        steps = set()

        # Walk into the hall
        if start in self.rooms:
            for i in range(i1 - 1, i2 - 1, -1):
                steps.add((i, j))
            assert i == i2

        # Walk down the hall
        dj = (j2 > j1) - (j1 > j2)
        for j in range(j1 + dj, j2 + dj, dj):
            steps.add((i, j))
        assert j == j2

        # Walk into a rooms
        if end in self.rooms:
            for i in range(i + 1, i2 + 1):
                steps.add((i, j))
        return steps

    def built_adjacent(self):
        adjacent = {}
        for i, j in self.rooms:
            if i == 2:
                adjacent[i, j] = {(1, j - 1), (1, j + 1)} & (
                    self.hall_dests | self.rooms
                )
            else:
                adjacent[i, j] = {(i - 1, j)} & (self.hall_dests | self.rooms)

        adjacent[1, 1] = {(1, 2)}
        adjacent[1, 11] = {(1, 10)}
        adjacent[1, 2] = {(2, 3), (1, 4)}
        adjacent[1, 10] = {(2, 9), (1, 8)}
        adjacent[1, 4] = {(2, 3), (2, 5), (1, 6)}
        adjacent[1, 8] = {(2, 9), (2, 7), (1, 6)}
        adjacent[1, 6] = {(2, 5), (2, 7), (1, 4), (1, 8)}
        return adjacent

    def build_path_map(self):
        path_map = {}
        for start in self.hall_dests:
            for end in self.rooms:
                path_map[start, end] = self.find_path(start, end)
        for start in self.rooms:
            for end in self.hall_dests:
                path_map[start, end] = self.find_path(start, end)
        path_map = {k: (v, len(v)) for (k, v) in path_map.items()}
        indirect_map = {}
        for s, e in path_map:
            if s not in indirect_map:
                indirect_map[s] = {}
            indirect_map[s][e] = path_map[s, e]
        return indirect_map

    def build_visitor_mask(self):
        visitor_mask = {}
        for kind, locs in self.amph_homes.items():
            visitor_mask[kind] = set()
            for other_kind in "ABCD":
                if kind != other_kind:
                    for loc in locs:
                        visitor_mask[kind].add((loc, other_kind))
        return visitor_mask

    def estimate_initial_cost(self, amphs, amph_homesets):
        estimate = 0
        n0 = self.amphs_per_type
        # Assume we have to move all items into final area
        for kind in "ABCD":
            estimate += COSTS[kind] * n0 * (n0 + 1) // 2
        for (i, j), kind in amphs:
            dj = abs(j - self.amph_home_j[kind])
            estimate += COSTS[kind] * (dj + (dj > 0) * (i - 1))
            # Subtract cost of items that are already there
            estimate -= COSTS[kind] * (dj == 0) * (i - 1)

        # for kind in "ABCD":
        #     estimate += COSTS[kind] * n0 * (n0 + 1) // 2
        return estimate

    def build_homesets(self):
        amph_homesets = {k: set() for k in "ABCD"}
        for k, locs in self.amph_homes.items():
            for loc in locs:
                amph_homesets[k].add((loc, k))
        return {k: frozenset(v) for (k, v) in amph_homesets.items()}

    def send_amphs_home(self, amphs):
        """
        >>> board = Board.from_text(EXAMPLE_TEXT)

        # >>> board.send_amphs_home(board.amphs)
        # 12521
        """

        path_map = self.build_path_map()
        visitor_mask = self.build_visitor_mask()
        hall_dests = self.hall_dests
        adjacent = self.built_adjacent()
        amph_homesets = self.build_homesets()
        amphs = frozenset(amphs.items())
        estimate = self.estimate_initial_cost(amphs, amph_homesets)
        n0 = self.amphs_per_type
        opendests = frozenset(self.hall)

        kind_props = {
            k: (
                amph_homesets[k],
                self.amph_homes[k],
                visitor_mask[k],
                COSTS[k],
                self.amph_home_j[k],
            )
            for k in "ABCD"
        }

        target = frozenset(self.target_amphs.items())

        queue = [(estimate, amphs, opendests)]
        best_score = inf
        scores = {}
        while queue:
            estimate, amphs, opendests = heappop(queue)
            for start, kind in amphs:
                if adjacent[start] & opendests:
                    # We can move from this position
                    homeset, homes, vmask, cost, target_j = kind_props[kind]
                    if start in hall_dests:
                        if amphs & vmask:
                            continue
                        # Try to move to the deepest available spot
                        ends = [max(homes & opendests)]
                    else:
                        ends = hall_dests & opendests
                        if not ends:
                            continue

                    # Remove the part of the score associated with start
                    if (dj := abs(start[1] - target_j)) == 0:
                        half_est = estimate - cost * (dj - (start[0] - 1))
                    else:
                        half_est = estimate - cost * (dj + (start[0] - 1))

                    end_2_path = path_map[start]
                    for end in ends:
                        path, cnt = end_2_path[end]
                        if not path.issubset(opendests):
                            continue
                        # Compute the new estimated score
                        if (dj := abs(end[1] - target_j)) == 0:
                            new_estimate = half_est + cost * (dj - (end[0] - 1) + cnt)
                        else:
                            new_estimate = half_est + cost * (dj + (end[0] - 1) + cnt)
                        if new_estimate >= best_score:
                            continue
                        new_amphs = amphs ^ {(start, kind), (end, kind)}
                        if new_amphs == target:
                            best_score = min(best_score, new_estimate)
                        else:
                            if (
                                new_amphs not in scores
                                or new_estimate < scores[new_amphs]
                            ):
                                scores[new_amphs] = new_estimate
                                heappush(
                                    queue,
                                    (new_estimate, new_amphs, opendests ^ {start, end}),
                                )
        return best_score


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
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

    target_board = TARGET_BOARD2

    @classmethod
    def from_text(cls, text):
        walls, amphs, hall = parse(augment_text(text))
        return cls(walls, amphs, hall)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
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
