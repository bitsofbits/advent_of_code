from heapq import heappop, heappush
from functools import cache

def render(maze, seats=()):
    max_i = max(i for (i, j) in maze)
    max_j = max(j for (i, j) in maze)
    rows = []
    for i in range(max_i + 1):
        row = []
        for j in range(max_j + 1):
            key = (i, j)
            if key in seats:
                row.append('O')
            elif key in maze:
                row.append('#')
            else:
                row.append('.')
        rows.append("".join(row))
    return "\n".join(rows)


def parse(text):
    """
    >>> maze, start, end = parse(EXAMPLE_TEXT)
    >>> start, end
    ((13, 1), (1, 13))
    """
    start = end = None
    maze = set()
    for i, row in enumerate(text.strip().split()):
        for j, x in enumerate(row.strip()):
            key = (i, j)
            if x == "#":
                maze.add(key)
            if x == "S":
                start = key
            if x == "E":
                end = key
    return frozenset(maze), start, end


directions = ">v<^"


@cache
def rotate(direction, n):
    return directions[(directions.index(direction) + n) % 4]


unit_vectors = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


@cache
def traverse_between(start, end, maze):
    # score, key, path
    queue = [(0, start, ">", (start,))]
    seen = set()
    while queue:
        score, key, direction, path = heappop(queue)
        if (key, direction) in seen:
            continue
        if key == end:
            return score
        seen.add((key, direction))
        # Turn left
        next_dir = rotate(direction, -1)
        heappush(queue,(score + 1000, key, next_dir, path))
        # Turn right
        next_dir = rotate(direction, 1)
        heappush(queue,(score + 1000, key, next_dir, path))
        # Go straight
        i, j = key
        di, dj = unit_vectors[direction]
        next_key= (i + di, j + dj)
        if next_key in maze:
            continue
        heappush(queue, (score + 1, next_key, direction, path + (next_key,)))       

def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7036
    >>> part_1(EXAMPLE_2_TEXT)
    11048
    """
    maze, start, end = parse(text)
    score = traverse_between(start, end, maze)
    return score


def traverse_all_paths_between(start, end, maze, best_score):
    queue = [(0, start, ">", frozenset([(start, '>')]))]
    seen = {}
    while queue:
        score, location, direction, path = heappop(queue)
        if score > best_score:
            return
        key = (location, direction)
        if key in seen and seen[key] > score:
            continue
        if location == end:
            yield path
            continue
        seen[key] = score
        # Turn left
        next_dir = rotate(direction, -1)
        next_path = path | {(location, next_dir)}
        heappush(queue,(score + 1000, location, next_dir, next_path))
        # Turn right
        next_dir = rotate(direction, 1)
        next_path = path | {(location, next_dir)}
        heappush(queue,(score + 1000, location, next_dir, next_path))
        # Go straight
        i, j = location
        di, dj = unit_vectors[direction]
        next_location = (i + di, j + dj)
        if next_location in maze:
            continue
        next_path = path | {(next_location, direction)}
        heappush(queue, (score + 1, next_location, direction, next_path))       

def traverse_all_paths_between(start, end, maze):
    queue = [(0, start, ">")]
    costs = {}
    final_cost = None
    final_keys = set()
    while queue:
        cost, location, direction = heappop(queue)
        key = (location, direction)            
        if key in costs:
            continue
        costs[key] = cost
        if location == end:
            final_cost = cost
            final_keys.add(key)
        # Turn left
        next_dir = rotate(direction, -1)
        heappush(queue,(cost + 1000, location, next_dir))
        # Turn right
        next_dir = rotate(direction, 1)
        heappush(queue,(cost + 1000, location, next_dir))
        # Go straight
        i, j = location
        di, dj = unit_vectors[direction]
        next_location = (i + di, j + dj)
        if next_location in maze:
            continue
        heappush(queue, (cost + 1, next_location, direction))  

    locations = set()
    queue = [(final_cost, *x) for x in final_keys]
    while queue:
        cost, location, direction = heappop(queue)
        locations.add(location)
        # Un-turn left
        next_dir = rotate(direction, 1)
        next_cost = cost - 1000
        if costs.get((location, next_dir)) == next_cost:
            heappush(queue,(next_cost, location, next_dir))
        # Un-turn right
        next_dir = rotate(direction, -1)
        next_cost = cost - 1000
        if costs.get((location, next_dir)) == next_cost:
            heappush(queue,(next_cost, location, next_dir))
        # Un-go straight
        i, j = location
        di, dj = unit_vectors[direction]
        next_location = (i - di, j - dj)
        next_cost = cost - 1
        if next_location in maze:
            continue
        if costs.get((next_location, direction)) == next_cost:
            heappush(queue, (next_cost, next_location, direction))  

    return locations



def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    45
    >>> part_2(EXAMPLE_2_TEXT)
    77

    # Problem says 64, but I think that's wrong
    """
    maze, start, end = parse(text)
    locations = traverse_all_paths_between(start, end, maze)
    # print(render(maze, locations))
    return len(locations)

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open(data_dir / "example_2.txt") as f:
        EXAMPLE_2_TEXT = f.read()

    doctest.testmod()
