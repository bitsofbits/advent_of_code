from collections import defaultdict
from functools import cache
from heapq import heappop, heappush
from math import inf


def parse_maze(text):
    walls = set()
    paths = set()
    chars = {}
    for i, row in enumerate(text.split('\n')):
        for j, x in enumerate(row):
            if x == '#':
                walls.add((i, j))
            elif x == '.':
                paths.add((i, j))
            elif x == ' ':
                pass
            else:
                chars[(i, j)] = x
    return walls, paths, chars


def find_extent(walls):
    i0 = min(i for (i, j) in walls)
    i1 = max(i for (i, j) in walls)
    j0 = min(j for (i, j) in walls)
    j1 = max(j for (i, j) in walls)
    return i0, i1, j0, j1


def find_inner_extent(walls, paths):
    i0, i1, j0, j1 = find_extent(walls)
    assert i0 == j0 == 2
    a0, a1 = i1, i0
    b0, b1 = j1, j0
    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            if (i, j) not in walls | paths:
                a0 = min(i, a0)
                a1 = max(i, a1)
                b0 = min(j, b0)
                b1 = max(j, b1)
    return a0, a1, b0, b1


def find_labels(walls, paths, chars):
    i0, i1, j0, j1 = find_extent(walls)
    a0, a1, b0, b1 = find_inner_extent(walls, paths)
    assert i0 == j0 == 2
    labels = {}
    for (i, j), x in chars.items():
        if i in (0, a0 + 1, a1 - 1, i1 + 2) or j in (0, b0 + 1, b1 - 1, j1 + 2):
            continue
        if i == 1:  # top
            labels[i0, j] = chars[0, j] + chars[1, j]
        elif i == a0:
            labels[a0 - 1, j] = chars[a0, j] + chars[a0 + 1, j]
        elif i == i1 + 1:
            labels[i1, j] = chars[i1 + 1, j] + chars[i1 + 2, j]
        elif i == a1:
            labels[a1 + 1, j] = chars[a1 - 1, j] + chars[a1, j]
        elif j == 1:  # left
            labels[i, j0] = chars[i, 0] + chars[i, 1]
        elif j == b0:
            labels[i, b0 - 1] = chars[i, b0] + chars[i, b0 + 1]
        elif j == j1 + 1:  # left
            labels[i, j1] = chars[i, j1 + 1] + chars[i, j1 + 2]
        elif j == b1:
            labels[i, b1 + 1] = chars[i, b1 - 1] + chars[i, b1]
        else:
            raise ValueError((i, j, x))
    assert sum(len(x) for x in labels) == len(chars)
    return labels


def render(walls, labels):
    i0, i1, j0, j1 = find_extent(walls)
    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            point = (i, j)
            if point in labels:
                chars.append(labels[point][-1])
            elif point in walls:
                chars.append('#')
            else:
                chars.append('•')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def parse(text):
    """
    >>> walls, paths, labels = parse(EXAMPLE_TEXT)
    >>> print(render(walls, labels))
    #################A#############
    #•#•••#•••••••••••••••••••#•#•#
    #•#•#•###•###•###•#########•#•#
    #•#•#•••••••#•••#•••••#•#•#•••#
    #•#########•###•#####•#•#•###•#
    #•••••••••••••#•#•••••#•••••••#
    ###•###########S###P#####•#•#•#
    #•••••#•••••••••••••••••#•#•#•#
    #######•••••••••••••••••#####•#
    #•#•••#•••••••••••••••••#•••••T
    #•#•#•#•••••••••••••••••#•#####
    #•••#•#•••••••••••••••••N•••#•#
    #•###•#•••••••••••••••••#####•#
    I•••#•#•••••••••••••••••#•••••#
    #####•#•••••••••••••••••#•###•#
    Z•••••#•••••••••••••••••G•••#•S
    ###•###•••••••••••••••••#######
    O•#•#•#•••••••••••••••••#•••••#
    #•#•#•#•••••••••••••••••###•#•#
    #•••#•I•••••••••••••••••U•••#•F
    #####•#•••••••••••••••••#•#####
    N•••••#•••••••••••••••••T•#•••G
    #•###•#•••••••••••••••••#•###•#
    #•#•••#•••••••••••••••••#•••••#
    ###•###•••••••••••••••••#•#•###
    #•••••#•••••••••••••••••#•#•••#
    #•###•#####O#F#####P#####•###•#
    #•••#•#•#•••#•••••#•••••#•#•••#
    #•#####•###•###•#•#•#########•#
    #•••#•#•••••#•••#•#•#•#•••••#•#
    #•###•#####•###•###•#•#•#######
    #•#•••••••••#•••#•••••••••••••#
    #########U###P###P#############
    """
    walls, paths, chars = parse_maze(text)
    labels = find_labels(walls, paths, chars)
    return walls, paths, labels


delta_ij = {(-1, 0), (0, 1), (1, 0), (0, -1)}


def build_graph(maze, labels, add_tunnels=True):
    # """
    # >>> board = parse(EXAMPLE_TEXT)
    # >>> edges, start, end = board_to_graph(board, slippery_deltas)
    # >>> start, end
    # (1, 527)
    # >>> sorted(edges)[:4]
    # [(1, 24), (24, 1), (24, 25), (25, 24)]
    # """

    width = max(j for (i, j) in maze | set(labels)) + 1

    def as_id(i, j):
        # assert j < width
        return i * width + j

    inverse_labels = defaultdict(set)
    for k, v in labels.items():
        inverse_labels[v].add(k)
    inverse_labels = dict(inverse_labels)

    [start] = inverse_labels['AA']
    [end] = inverse_labels['ZZ']

    edges = []
    for i, j in maze:
        for di, dj in delta_ij:
            i1 = i + di
            j1 = j + dj
            if (i1, j1) in maze:
                edges.append(((i, j), (i1, j1)))

    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)

    for label_targets in inverse_labels.values():
        assert len(label_targets) in (1, 2)
        if len(label_targets) == 2:
            nd1, nd2 = label_targets
            assert nd1 in nodes, nd1
            assert nd2 in nodes, nd2
            if add_tunnels:
                edges.append((nd1, nd2))
                edges.append((nd2, nd1))

    i0, i1, j0, j1 = find_extent(maze)

    def is_outer(i, j):
        return i in (i0, i1) or j in (j0, j1)

    return (
        frozenset((as_id(*a), as_id(*b)) for (a, b) in edges),
        as_id(*start),
        as_id(*end),
        {as_id(*k): v for (k, v) in labels.items() if is_outer(*k)},
        {as_id(*k): v for (k, v) in labels.items() if not is_outer(*k)},
    )


def traverse_graph(edges, start, end):
    queue = [(0, start)]
    targets = {}
    for src, tgt in edges:
        if src not in targets:
            targets[src] = set()
        if tgt not in targets:
            targets[tgt] = set()
        targets[src].add(tgt)

    assert start in targets, start
    assert end in targets, end

    seen = set()
    while queue:
        count, node = heappop(queue)
        if node in seen:
            continue
        if node == end:
            return count
        seen.add(node)
        for next_node in targets[node]:
            next_count = count + 1
            heappush(queue, (next_count, next_node))


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    58
    """
    walls, maze, labels = parse(text)
    edges, start, end, _, _ = build_graph(maze, labels)
    return traverse_graph(edges, start, end)


def traverse_graph_reciprocal(edges, outer_labels, inner_labels, start, end):
    # label_nodes = set(outer_labels) | set(inner_labels)
    # edges = simplify_edges(edges, start, end, should_preserve=label_nodes)

    inverse_outer_labels = {}
    for k, v in outer_labels.items():
        inverse_outer_labels[v] = k
    inverse_inner_labels = {}
    for k, v in inner_labels.items():
        inverse_inner_labels[v] = k

    outer_labels = {}
    inner_labels = {}
    for k, inner_node in inverse_inner_labels.items():
        outer_node = inverse_outer_labels[k]
        outer_labels[outer_node] = inner_node
        inner_labels[inner_node] = outer_node

    queue = [(1, 0, start)]

    targets = {}
    for src, tgt in edges:
        if src not in targets:
            targets[src] = set()
        if tgt not in targets:
            targets[tgt] = set()
        targets[src].add(tgt)

    @cache
    def get_targets(node, level):
        tgts = {(tgt, level) for tgt in targets[node]}
        if node in outer_labels and level > 1:
            tgts.add((outer_labels[node], level - 1))
        if node in inner_labels and level <= len(inverse_inner_labels):
            tgts.add((inner_labels[node], level + 1))
        return tgts

    seen = set()
    while queue:
        level, count, node = heappop(queue)
        state = (level, node)
        if state in seen:
            continue
        if node == end and level == 1:
            return count
        seen.add(state)
        for next_node, next_level in get_targets(node, level):
            next_count = count + 1
            heappush(
                queue,
                (next_level, next_count, next_node),
            )


def build_recursed_graph(maze, labels):
    edges, start, end, outer_labels, inner_labels = build_graph(
        maze, labels, add_tunnels=False
    )


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    396
    """
    walls, maze, labels = parse(text)
    edges, start, end, outer_labels, inner_labels = build_graph(
        maze, labels, add_tunnels=False
    )
    return traverse_graph_reciprocal(edges, outer_labels, inner_labels, start, end)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
