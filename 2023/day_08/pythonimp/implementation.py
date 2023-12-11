import math
from itertools import count, cycle


def parse(text):
    """
    >>> _ = parse(EXAMPLE_TEXT)
    """
    instructions, raw_nodes = text.strip().split('\n\n')
    nodes = {}
    for line in raw_nodes.split('\n'):
        key, value_text = line.split(' = ')
        left, right = tuple(value_text[1:-1].split(', '))
        nodes[key] = (left, right)
    return instructions.strip(), nodes


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    >>> part_1(EXAMPLE2_TEXT)
    6
    """
    instructions, node_map = parse(text)
    node = "AAA"
    for n_steps, instruction in enumerate(cycle(instructions)):
        if node == "ZZZ":
            break
        i = "LR".index(instruction)
        node = node_map[node][i]
    return n_steps


def find_cycle(node, instructions, node_map):
    seen_at = {}
    end_at = []
    for i, instruction in enumerate(cycle(instructions)):
        if node.endswith('Z'):
            end_at.append(i)
        if node in seen_at:
            if (i - seen_at[node]) % len(instructions) == 0:
                break
        else:
            seen_at[node] = i
        is_right = "LR".index(instruction)
        node = node_map[node][is_right]
    loop_start = seen_at[node]
    loop_length = i - seen_at[node]
    return loop_start, loop_length, end_at


def find_nodes_ending_in_A(node_map):
    nodes = set()
    for k, (l, r) in node_map.items():
        for node in (k, l, r):
            if node.endswith('A'):
                nodes.add(node)
    return nodes


def merge_cycles(start_1, length_1, start_2, length_2):
    assert 0 <= start_1 < length_1
    assert 0 <= start_2 < length_2

    if length_2 > length_1:
        start_1, start_2 = start_2, start_1
        length_1, length_2 = length_2, length_1
    length = length_1 * length_2 / math.gcd(int(length_1), int(length_2))
    assert length % 1 == 0
    length = int(length)
    for i in range(length // length_1):
        start = start_1 + i * length_1
        if start % length_2 == start_2:
            break
    else:
        return None
    assert 0 <= start < length
    return start, length


def part_2(text):
    """
    >>> part_2(EXAMPLE3_TEXT)
    6

    14265111103729
    """
    instructions, node_map = parse(text)
    nodes = find_nodes_ending_in_A(node_map)

    cycles = {}
    for node in nodes:
        cycles[node] = find_cycle(node, instructions, node_map)

    # Really we should check before the first cycle for all of these
    # but assume minimum occurs after that.
    compute_cycles = []
    max_start = max(start for (start, *_) in cycles.values())
    for node in sorted(cycles.keys(), key=lambda k: cycles[k][1], reverse=True):
        loop_start, loop_length, end_at = cycles[node]
        relative_ends = set()
        for i in range(loop_length):
            n = max_start + i
            for end in end_at:
                if (end >= loop_start) and (
                    end - max_start
                ) % loop_length == n - max_start:
                    relative_ends.add(i)
        compute_cycles.append((max_start, loop_length, sorted(relative_ends)))

    _, length, ends = compute_cycles[0]
    merged_cycles = [(end, length) for end in ends]
    for _, l1, ends in compute_cycles[1:]:
        new_merged = []
        for e0, l0 in merged_cycles:
            for e1 in ends:
                merged = merge_cycles(e0, l0, e1, l1)
                if merged is not None:
                    new_merged.append(merged)
        merged_cycles = new_merged
    return min(start + max_start for (start, _) in merged_cycles)


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
