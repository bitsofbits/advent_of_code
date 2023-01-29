from functools import cache
from heapq import heappop, heappush
from math import inf

floors = ["first", "second", "third", "fourth"]


def parse_chunk(chunk):
    _, a, b = chunk.strip().split()
    if "-" in a:
        a, _ = a.split("-")
    b = b.strip(",")
    assert b in {"microchip", "generator"}, b
    return (a, b)


def parse_line(line):
    _, f, _, _, rest = line.strip().rstrip(".").split(maxsplit=4)
    f = floors.index(f)
    if "and" in rest:
        rest, obj = rest.split(" and ")
        chunks = [obj] + rest.split(", ")
    elif rest.strip() == "nothing relevant":
        chunks = []
    else:
        chunks = [rest]
    return f, [parse_chunk(x) for x in chunks]


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    (0, [('lithium', 'microchip'), ('hydrogen', 'microchip')])
    (1, [('hydrogen', 'generator')])
    (2, [('lithium', 'generator')])
    (3, [])
    """
    for line in text.strip().split("\n"):
        yield (parse_line(line))


@cache
def safe(items):
    """
    >>> safe(())
    True
    >>> safe((('lithium', 'microchip'), ('hydrogen', 'generator')))
    False
    >>> safe((('lithium', 'microchip'),))
    True
    >>> safe((('lithium', 'microchip'), ('hydrogen', 'microchip')))
    True
    >>> safe((('lithium', 'generator'), ('hydrogen', 'generator')))
    True
    >>> safe((('lithium', 'generator'), ('hydrogen', 'generator'),
    ...        ('lithium', 'microchip')))
    True
    >>> safe((('lithium', 'generator'), ('hydrogen', 'generator'),
    ...        ('lithium', 'microchip'), ('spam', "microchip")))
    False
    """
    gens = set(x for (x, kind) in items if kind == "generator")
    chips = set(x for (x, kind) in items if kind == "microchip")
    assert len(chips) + len(gens) == len(items), (chips, gens, items)
    return (not gens) or (not (chips - gens))


@cache
def floor_state(f):
    return (
        sum(1 for (_, k) in f if k == "microchip"),
        sum(1 for (_, k) in f if k == "generator"),
    )


def state(floors):
    return tuple(floor_state(f) for f in floors)


def move_stuff(starting_floors):
    assert len(starting_floors) == 4
    item_count = sum(len(x) for x in starting_floors)
    lowest_cnt = inf
    initial_est = sum((3 - i) * len(x) / 2 for (i, x) in enumerate(starting_floors))
    states = {}
    queue = [(initial_est, 0, 0, starting_floors)]
    while queue:
        estimate, cnt, flr, floors = heappop(queue)
        if len(floors[3]) == item_count:
            assert estimate == cnt
            lowest_cnt = min(cnt, lowest_cnt)
            continue
        next_cnt = cnt + 1
        for item_1 in floors[flr]:
            for item_2 in floors[flr]:
                if item_2 > item_1:
                    continue
                moved = {item_1, item_2}
                if not safe(floors[flr] - moved):
                    continue
                # We can move up or down one floor
                for next_flr in [flr - 1, flr + 1]:
                    if not 0 <= next_flr < 4:
                        continue
                    if not safe(floors[next_flr] | moved):
                        continue
                    next_floors = tuple(
                        {flr: x - moved, next_flr: x | moved}.get(i, x)
                        for (i, x) in enumerate(floors)
                    )
                    key = (next_flr, state(next_floors))
                    if next_cnt >= states.get(key, inf):
                        continue
                    states[key] = next_cnt
                    next_estimate = estimate + 1 - (next_flr - flr) * len(moved) / 2
                    heappush(queue, (next_estimate, next_cnt, next_flr, next_floors))
    return lowest_cnt


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)  # 47 for data
    11
    """
    floors = [None] * 4
    for k, v in parse(text):
        floors[k] = frozenset(v)
    floors = tuple(floors)
    return move_stuff(floors)


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    35
    """
    floors = [None] * 4
    for k, v in parse(text):
        floors[k] = frozenset(v)
    floors[0] |= {
        ("elerium", "microchip"),
        ("dilithium", "microchip"),
        ("elerium", "generator"),
        ("dilithium", "generator"),
    }
    floors = tuple(floors)
    return move_stuff(floors)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    EXAMPLE2_TEXT = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator and a lithium generator.
The third floor contains nothing relevant.
The fourth floor contains nothing relevant.
    """

    doctest.testmod()
