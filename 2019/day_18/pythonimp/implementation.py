from heapq import heappop, heappush
from math import inf


class SortableDict(dict):
    def __lt__(self, other):
        return id(self) < id(other)


def parse(text):
    """
    >>> walls, entrance, doors, keys = parse(EXAMPLE_TEXT)
    >>> sorted(keys.items())[:4]
    [((1, 16), 'b'), ((1, 22), 'f'), ((3, 8), 'a'), ((3, 12), 'c')]
    >>> sorted(doors.items())
    [((1, 18), 'C'), ((1, 20), 'D'), ((3, 10), 'B'), ((3, 16), 'A'), ((3, 20), 'F')]
    """
    walls = set()
    entrance = None
    doors = {}
    keys = {}
    for i, row in enumerate(text.strip().split('\n')):
        for j, x in enumerate(row):
            point = (i, j)
            if x == '#':
                walls.add(point)
            elif x == '@':
                entrance = point
            elif x.islower():
                keys[point] = x
            elif x.isupper():
                doors[point] = x
            else:
                assert x == '.', x
    return frozenset(walls), entrance, doors, keys


delta_ij = {(-1, 0), (0, 1), (1, 0), (0, -1)}


def build_graph(text):
    # """
    # >>> board = parse(EXAMPLE_TEXT)
    # >>> edges, start, end = board_to_graph(board, slippery_deltas)
    # >>> start, end
    # (1, 527)
    # >>> sorted(edges)[:4]
    # [(1, 24), (24, 1), (24, 25), (25, 24)]
    # """
    board = text.strip().split('\n')
    height = len(board)
    width = len(board[0])

    def as_id(i, j):
        return i * width + j

    nodes = {
        (i, j): x
        for (i, row) in enumerate(board)
        for (j, x) in enumerate(row)
        if x != '#'
    }

    keys = {
        as_id(i, j): x
        for (i, row) in enumerate(board)
        for (j, x) in enumerate(row)
        if 'a' <= x <= 'z'
    }

    doors = {
        as_id(i, j): x
        for (i, row) in enumerate(board)
        for (j, x) in enumerate(row)
        if 'A' <= x <= 'Z'
    }

    entrances = frozenset(
        {
            as_id(i, j)
            for (i, row) in enumerate(board)
            for (j, x) in enumerate(row)
            if x == '@'
        }
    )

    edges = []
    for (i, j), x in nodes.items():
        for di, dj in delta_ij:
            if 0 <= (i1 := i + di) < height and 0 <= (j1 := j + dj) < width:
                if board[i1][j1] != '#':
                    edges.append(((i, j), (i1, j1)))
                    assert (i1, j1) in nodes

    return (
        frozenset((as_id(*a), as_id(*b)) for (a, b) in edges),
        entrances,
        doors,
        keys,
    )


def simplify(edges, preserve):
    label_set = set()
    for nd1, nd2 in edges:
        label_set.add(nd1)
        label_set.add(nd2)
    labels = sorted(label_set)

    cost = {(i, j): inf for i in labels for j in labels}
    for nd1, nd2 in edges:
        cost[nd1, nd2] = 1
        cost[nd2, nd1] = 1
        cost[nd1, nd1] = cost[nd2, nd2] = 0
    for k in labels:
        for i in labels:
            for j in labels:
                cost[i, j] = min(cost[i, j], cost[i, k] + cost[k, j])

    new_edges = []
    for nd1 in preserve:
        for nd2 in preserve:
            if nd1 != nd2:
                new_edges[nd1, nd2] = cost[nd1, nd2]

    return new_edges


def simplify_edges(edges, entrances, doors, keys):
    nodes = set(x[0] for x in edges) | set(x[1] for x in edges)
    should_preserve = set(entrances) | set(doors) | set(keys)
    new_edges = [(s, t, 1) for (s, t) in edges]

    inputs = {}
    outputs = {}
    weights = {}
    nodes = set(x[0] for x in new_edges) | set(x[1] for x in new_edges)
    for nd1 in nodes:
        for nd2 in nodes:
            weights[nd1, nd2] = inf
        weights[nd1, nd1] = 1

    for source, target, weight in new_edges:
        if target not in inputs:
            inputs[target] = set()
        inputs[target].add(source)
        if source not in outputs:
            outputs[source] = set()
        outputs[source].add(target)
        weights[source, target] = weight

    # remove all nodes with single outputs since they are dead ends
    while True:
        for node in nodes:
            if node in should_preserve:
                continue
            if len(outputs[node]) != len(inputs[node]):
                continue
            assert len(outputs[node]) != 0
            if len(outputs[node]) != 1:
                continue
            assert outputs[node] == inputs[node]

            [nbr] = outputs[node]

            outputs[nbr] = {x for x in outputs.get(nbr, ()) if x != node}
            inputs[nbr] = {x for x in inputs.get(nbr, ()) if x != node}
            weights.pop((node, nbr), 0)
            weights.pop((nbr, node), 0)
            weights.pop((node, node))
            inputs.pop(node)
            outputs.pop(node)
            nodes.remove(node)
            break
        else:
            break

    # Reduce all runs of points to single edge
    while True:
        for node in nodes:
            if node in should_preserve:
                continue
            if len(outputs[node]) != len(inputs[node]):
                continue
            assert len(outputs[node]) > 1
            if len(outputs[node]) > 2:
                continue

            assert outputs[node] == inputs[node]
            neighbors = outputs[node]

            new_weights = {}
            for child in neighbors:
                for parent in neighbors:
                    assert child != node
                    assert parent != node
                    if child != parent:
                        new_weights[parent, child] = min(
                            weights[parent, child],
                            weights[parent, node] + weights[node, child],
                        )
                        outputs[parent] = {
                            child if (x == node) else x
                            for x in outputs.get(parent, ())
                            if x != parent
                        }
                        inputs[child] = {
                            parent if (x == node) else x
                            for x in inputs.get(child, ())
                            if x != child
                        }
                        assert node not in outputs[parent]
                        assert node not in inputs[child]
            weights.update(new_weights)
            for nbr in neighbors:
                weights.pop((node, nbr), 0)
                weights.pop((nbr, node), 0)
            weights.pop((node, node))
            inputs.pop(node)
            outputs.pop(node)
            nodes.remove(node)
            assert node not in should_preserve
            break
        else:
            break

    new_edges = []
    for source in nodes:
        for target in nodes:
            if source == target:
                continue
            wt = weights[source, target]
            assert wt != 0
            if wt < 1e6:
                assert weights[target, source] == weights[source, target]
                new_edges.append((source, target, weights[source, target]))

    # print(new_edges)

    return new_edges


# def traverse(walls, entrance, doors, keys):
#     queue = [(0, len(doors), entrance, SortableDict(doors), SortableDict(keys))]
#     seen = set()
#     while queue:
#         count, _, (i, j), doors, keys = heappop(queue)
#         state = (i, j, frozenset(doors), frozenset(keys))
#         if state in seen:
#             continue
#         if not keys:
#             return count
#         seen.add(state)
#         next_count = count + 1
#         for di, dj in delta_ij:
#             next_point = (i + di, j + dj)
#             if next_point in walls or next_point in doors:
#                 continue
#             if next_point in keys:
#                 next_keys = SortableDict(keys)
#                 door = next_keys[next_point].upper()
#                 del next_keys[next_point]
#                 for k, v in doors.items():
#                     if v == door:
#                         break
#                 else:
#                     k = None
#                 if k is not None:
#                     next_doors = SortableDict(doors)
#                     del next_doors[k]
#                 else:
#                     next_doors = doors
#             else:
#                 next_keys = keys
#                 next_doors = doors
#             heappush(
#                 queue, (next_count, len(next_doors), next_point, next_doors, next_keys)
#             )
#     raise ValueError("couldn't find all keys")


# def part_1(text):
#     """
#     >>> part_1(EXAMPLE_TEXT)
#     132
#     >>> part_1(EXAMPLE2_TEXT)
#     136
#     """
#     walls, entrance, doors, keys = parse(text)
#     count = traverse(walls, entrance, doors, keys)
#     return count


def traverse_graph(edges, entrances, door_map, key_map):
    edges = simplify_edges(edges, entrances, door_map, key_map)
    inverse_door_map = {v: k for (k, v) in door_map.items()}
    key_to_door_map = {
        k: inverse_door_map[v.upper()]
        for (k, v) in key_map.items()
        if v.upper() in inverse_door_map
    }
    initial_robots = tuple(sorted(entrances))
    queue = [
        (
            0,
            0,
            initial_robots,
            frozenset(door_map),
            frozenset(key_map),
        )
    ]
    targets = {}
    for src, tgt, cost in edges:
        if src not in targets:
            targets[src] = set()
        if tgt not in targets:
            targets[tgt] = set()
        targets[src].add((tgt, cost))

    seen = set(initial_robots)
    while queue:
        _, count, robots, doors, keys = heappop(queue)
        state = (robots, doors, keys)
        if state in seen:
            continue
        if not keys:
            return count
        seen.add(state)
        for n, node in enumerate(robots):
            for next_node, cost in targets[node]:
                if next_node in doors:
                    continue
                next_count = count + cost
                next_doors = doors
                next_keys = keys
                if next_node in keys:
                    next_keys = keys - {next_node}
                    if next_node in key_to_door_map:
                        next_doors = doors - {key_to_door_map[next_node]}
                next_robots = robots[:n] + (next_node,) + robots[n + 1 :]
                heappush(
                    queue,
                    (
                        next_count,
                        next_count,
                        next_robots,
                        next_doors,
                        next_keys,
                    ),
                )
    # raise ValueError("couldn't find all keys")


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    132
    >>> part_1(EXAMPLE2_TEXT)
    136
    """
    # walls, entrance, doors, keys = parse(text)
    edges, entrances, doors, keys = build_graph(text)
    return traverse_graph(edges, entrances, doors, keys)
    # count = traverse(walls, entrance, doors, keys)
    # return count


replacement = """
@#@
###
@#@
""".strip()


def modify_map(walls, entrance, doors, keys):
    i0, j0 = (x - 1 for x in entrance)
    entrances = []
    walls = set(walls)
    for di, row in enumerate(replacement.split('\n')):
        for dj, x in enumerate(row):
            i = i0 + di
            j = j0 + dj
            if x == '#':
                walls.add((i, j))
            elif x == '@':
                entrances.append((i, j))
            assert (i, j) not in doors
            assert (i, j) not in keys
    return frozenset(walls), tuple(entrances)


# # If this turns out to be too slow, can collapse into simplified graph
# # (a) turn to graph, (b) simplify straight chunks
# # See 2023 day 23 as an example
# def multi_traverse(walls, entrances, doors, keys):
#     assert len(entrances) == 4
#     queue = [(0, len(keys), entrances, SortableDict(doors), SortableDict(keys))]
#     seen = set()
#     while queue:
#         count, _, robots, doors, keys = heappop(queue)
#         state = (robots, frozenset(doors), frozenset(keys))
#         if state in seen:
#             continue
#         if not keys:
#             return count
#         seen.add(state)
#         next_count = count + 1
#         for n, robot in enumerate(robots):
#             i, j = robot
#             for di, dj in delta_ij:
#                 next_point = (i + di, j + dj)
#                 if next_point in walls or next_point in doors:
#                     continue
#                 if next_point in keys:
#                     next_keys = SortableDict(keys)
#                     door = next_keys[next_point].upper()
#                     del next_keys[next_point]
#                     for k, v in doors.items():
#                         if v == door:
#                             break
#                     else:
#                         k = None
#                     if k is not None:
#                         next_doors = SortableDict(doors)
#                         del next_doors[k]
#                     else:
#                         next_doors = doors
#                 else:
#                     next_keys = keys
#                     next_doors = doors
#                 next_robots = robots[:n] + (next_point,) + robots[n + 1 :]
#                 heappush(
#                     queue,
#                     (next_count, len(next_keys), next_robots, next_doors, next_keys),
#                 )
#     raise ValueError("couldn't find all keys")


def render(walls, entrances, doors, keys):
    i0 = min(i for (i, j) in walls)
    i1 = max(i for (i, j) in walls)
    j0 = min(j for (i, j) in walls)
    j1 = max(j for (i, j) in walls)

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            point = (i, j)
            if point in entrances:
                chars.append('@')
            elif point in walls:
                chars.append('#')
            elif point in keys:
                chars.append(keys[point])
            elif point in doors:
                chars.append(doors[point])
            else:
                chars.append('.')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def part_2(text):
    """
    >>> part_2(EXAMPLE3_TEXT)
    32
    >>> part_2(EXAMPLE4_TEXT)
    72

    1724
    """
    walls, entrance, doors, keys = parse(text)
    walls, entrances = modify_map(walls, entrance, doors, keys)
    image = render(walls, entrances, doors, keys)
    edges, entrances, doors, keys = build_graph(image)
    return traverse_graph(edges, entrances, doors, keys)

    # return multi_traverse(walls, entrances, doors, keys)


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
    with open(data_dir / "example4.txt") as f:
        EXAMPLE4_TEXT = f.read()
    doctest.testmod()
