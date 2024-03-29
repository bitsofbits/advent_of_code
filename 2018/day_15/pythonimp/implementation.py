from heapq import heappop, heappush
from itertools import count
from math import inf

# , isinf


def render(board, elves=(), goblins=(), distances=()):
    i0 = min(i for ((i, j)) in board)
    i1 = max(i for ((i, j)) in board) + 1
    j0 = min(j for ((i, j)) in board)
    j1 = max(j for ((i, j)) in board) + 1
    rows = []
    for i in range(i0, i1):
        row = []
        for j in range(j0, j1):
            key = (i, j)
            if key in board:
                row.append('#')
            elif key in elves:
                row.append('E')
            elif key in goblins:
                row.append('G')
            elif key in distances:
                row.append(hex(distances[key])[-1:])
            else:
                row.append('.')
        rows.append(''.join(row))
    return '\n'.join(rows)


def parse(text):
    """
    >>> board, elves, goblins = parse(EXAMPLE_TEXT)

    # >>> print(render(board, elves, goblins))
    # #########
    # #G..G..G#
    # #.......#
    # #.......#
    # #G..E..G#
    # #.......#
    # #.......#
    # #G..G..G#
    # #########
    """
    board = set()
    elves = set()
    goblins = set()
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            key = (i, j)
            if x == '#':
                board.add(key)
            if x == 'G':
                goblins.add(key)
            if x == 'E':
                elves.add(key)
    return board, elves, goblins


# Note these are in read order
moves = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def find_cells_in_range_of(targets, occupied_space):
    in_range_of = set()
    for i, j in targets:
        for di, dj in moves:
            location = (i + di, j + dj)
            if location not in occupied_space:
                in_range_of.add(location)
    return in_range_of


def shortest_paths_from(root, occupied_space):
    queue = [(0, root)]
    shortest_paths = {}
    while queue:
        steps, location = heappop(queue)
        if location in shortest_paths:
            continue
        shortest_paths[location] = steps
        i, j = location
        next_steps = steps + 1
        for di, dj in moves:
            next_location = (i + di, j + dj)
            if next_location not in occupied_space:
                heappush(queue, (next_steps, next_location))
    return shortest_paths


def find_path_to(destination, distances):
    # TODO: this may not be right == may need to do inverse path finding :-()

    last_x = x = destination
    while distances[x]:
        last_x = x
        candidates = [(x[0] + di, x[1] + dj) for (di, dj) in moves]
        x = min(candidates, key=lambda x: (distances.get(x, inf), x))
    return last_x


def find_first_step_from(start, end, occupied_space):
    # TODO: this may not be right == may need to do inverse path finding :-()
    distances = shortest_paths_from(end, occupied_space)
    i, j = start
    candidates = [(i + di, j + dj) for (di, dj) in moves]
    return min(candidates, key=lambda x: (distances.get(x, inf), x))


def summarize(units, board, combat_round):
    # No more targets, simulation is over
    elves = [(i, j) for (i, j, _, is_elf_i) in units if is_elf_i is True]
    goblins = [(i, j) for (i, j, _, is_elf_i) in units if is_elf_i is False]
    print(render(board, elves=elves, goblins=goblins))
    print()
    # for i in range(ndx + 1, len(units)):
    #     if units[i][-1] is not None:
    #         # round not complete
    #         combat_round -= 1
    #         break
    complete_combat_rounds = combat_round - 1

    remaining_hp = sum(hp for (i, j, hp, is_elf) in units if is_elf is not None)
    return complete_combat_rounds, remaining_hp, complete_combat_rounds * remaining_hp


def simulate(board, units, elf_attack_power=3):
    for combat_round in count(1):
        units.sort()
        for ndx0, (i0, j0, hit_points_0, is_elf_0) in enumerate(units):
            if is_elf_0 is None:
                # This unit has been removed so skip
                continue

            # Find all of the potential targets
            # They have the opposite value of is_elf
            # Note this ignores removed items
            target_is_elf = not is_elf_0
            targets = [
                (i1, j1)
                for (i1, j1, _, is_elf_1) in units
                if is_elf_1 is not None and is_elf_1 == target_is_elf
            ]
            if len(targets) == 0:
                return units, combat_round

            # Occupied space consists of all the walls (board) plus all the units
            # that are still present except where current unit is.
            occupied_space = board | {
                (i1, j1)
                for (i1, j1, _, is_elf_1) in units
                if is_elf_1 is not None and (i1, j1) != (i0, j0)
            }

            # Also find all the places we might want to go -- that is all cells adjacent
            # to a target
            available_dests = find_cells_in_range_of(targets, occupied_space)

            if (i0, j0) in available_dests:
                destination = (i0, j0)
            else:
                # Find map of shortest distance from current unit to everywhere on board
                # -- can be used to efficiently find where to process
                distances = shortest_paths_from((i0, j0), occupied_space)

                if not (available_dests & set(distances)):
                    # No reachable destinations
                    continue

                destination = min(
                    available_dests, key=lambda x: (distances.get(x, inf), x)
                )

                assert distances[destination] != 0

                destination = find_first_step_from(
                    (i0, j0), destination, occupied_space
                )

                # i1, j1 = destination = find_path_to(destination, distances)
                units[ndx0] = (*destination, hit_points_0, is_elf_0)
                # continue

                # if distances[destination] != 0:
                #     continue

            i1, j1 = destination
            full_targets = []
            for di, dj in moves:
                if (i1 + di, j1 + dj) in targets:
                    for ndx2, (i2, j2, hit_points_2, is_elf_2) in enumerate(units):
                        if is_elf_2 == target_is_elf and (i2, j2) == (i1 + di, j1 + dj):
                            full_targets.append(ndx2)
            if not full_targets:
                continue

            ndx2 = min(
                full_targets, key=lambda i: (units[i][2], units[i][0], units[i][1])
            )
            i2, j2, hit_points_2, is_elf_2 = units[ndx2]
            assert is_elf_0 is not None
            assert hit_points_2 > 0 and is_elf_2 is not None and is_elf_2 != is_elf_0
            attack_power = elf_attack_power if is_elf_0 else 3
            hit_points_2 -= attack_power
            if hit_points_2 <= 0:
                is_elf_2 = None
            units[ndx2] = (i2, j2, hit_points_2, is_elf_2)


def part_1(text, always_summarize=False):
    """
    # >>> part_1(EXAMPLE_TEXT, always_summarize=True)

    >>> part_1(EXAMPLE2_TEXT)
    #######
    #...#E#
    #E#...#
    #.E##.#
    #E..#E#
    #.....#
    #######
    <BLANKLINE>
    (37, 982, 36334)
    >>> part_1(EXAMPLE3_TEXT)
    #######
    #.E.E.#
    #.#E..#
    #E.##.#
    #.E.#.#
    #...#.#
    #######
    <BLANKLINE>
    (46, 859, 39514)
    """
    board, elves, goblins = parse(text)
    units = [(i, j, 200, True) for (i, j) in elves] + [
        (i, j, 200, False) for (i, j) in goblins
    ]
    units, combat_round = simulate(board, units)
    return summarize(units, board, combat_round)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    #######
    #..E..#
    #...E.#
    #.#.#.#
    #...#.#
    #.....#
    #######
    <BLANKLINE>
    (15, 29, 172, 4988)
    >>> part_2(EXAMPLE2_TEXT)

    >>> part_2(EXAMPLE3_TEXT)
    #######
    #.E.#E#
    #E#...#
    #.E##.#
    #E..#E#
    #.....#
    #######
    <BLANKLINE>
    (4, 33, 948, 31284)


    37 * 94 = 3478
    """
    board, elves, goblins = parse(text)
    for elf_attack_power in count(3):
        units = [(i, j, 200, True) for (i, j) in elves] + [
            (i, j, 200, False) for (i, j) in goblins
        ]
        units, combat_round = simulate(board, units, elf_attack_power=elf_attack_power)
        n_surviving_elves = len([x for x in units if x[-1]])
        # print(elf_attack_power, n_surviving_elves, len(elves))
        if n_surviving_elves == len(elves):
            return (elf_attack_power,) + summarize(units, board, combat_round)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "example3.txt") as f:
        EXAMPLE3_TEXT = f.read()
    doctest.testmod()
