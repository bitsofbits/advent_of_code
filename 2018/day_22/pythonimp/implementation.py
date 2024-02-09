from functools import cache
from heapq import heappop, heappush


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    (510, (10, 10))
    """
    a, b = text.strip().split('\n')
    assert a.startswith('depth:')
    assert b.startswith('target:')
    depth = int(a.split()[-1])
    target = b.split()[-1]
    target = tuple(int(x.strip()) for x in target.split(','))
    return depth, target


@cache
def compute_erosion(x, y, target, depth):
    if x < 0 or y < 0:
        raise ValueError((x, y))
    if x == y == 0:
        return depth % 20183
    if (x, y) == target:
        return depth % 20183
    if x == 0:
        return (y * 48271 + depth) % 20183
    if y == 0:
        return (x * 16807 + depth) % 20183
    a = compute_erosion(x, y - 1, target, depth)
    b = compute_erosion(x - 1, y, target, depth)
    return ((a * b) + depth) % 20183


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    114

    9899
    """
    depth, target = parse(text)
    total = 0
    for x in range(0, target[0] + 1):
        for y in range(0, target[1] + 1):
            total += compute_erosion(x, y, target, depth) % 3
    return total


# In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
# In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
# In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).

NEITHER = 0
CLIMBING_GEAR = 1
TORCH = 2

ROCKY = 0
WET = 1
NARROW = 2


def is_compatible(gear, terrain):
    if terrain == ROCKY:
        return gear in (CLIMBING_GEAR, TORCH)
    if terrain == WET:
        return gear in (CLIMBING_GEAR, NEITHER)
    if terrain == NARROW:
        return gear in (TORCH, NEITHER)


def traverse(target, depth):
    def terrain(x, y):
        return compute_erosion(x, y, target, depth) % 3

    queue = [(0, 0, 0, TORCH)]
    seen = set()
    while queue:
        time, x, y, gear = heappop(queue)
        key = (x, y, gear)
        if key in seen:
            continue
        seen.add(key)

        if (x, y) == target and gear == TORCH:
            return time
        # Stand still and change gear
        for next_gear in [NEITHER, CLIMBING_GEAR, TORCH]:
            if next_gear != gear:
                heappush(queue, (time + 7, x, y, next_gear))
        # Or move
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            next_x = x + dx
            next_y = y + dy
            if next_x < 0 or next_y < 0:
                continue
            if not is_compatible(gear, terrain(next_x, next_y)):
                continue
            queue.append((time + 1, next_x, next_y, gear))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    45
    """
    depth, target = parse(text)
    return traverse(target, depth)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
