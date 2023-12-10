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
    for count, instruction in enumerate(cycle(instructions)):
        if node == "ZZZ":
            break
        i = "LR".index(instruction)
        node = node_map[node][i]
    return count


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
        i = "LR".index(instruction)
        node = node_map[node][i]
    loop_start = seen_at[node]
    loop_length = i - seen_at[node]
    return loop_start, loop_length, end_at


def part_2(text):
    """
    >>> part_2(EXAMPLE3_TEXT)
    6
    """
    instructions, node_map = parse(text)
    nodes = set()
    for k, (l, r) in node_map.items():
        for node in (k, l, r):
            if node.endswith('A'):
                nodes.add(node)
    cycles = {}
    print(nodes)
    for node in nodes:
        cycles[node] = find_cycle(node, instructions, node_map)
    # Really we should check before the first cycle for all of these
    # but assume minimum occurs after that.
    compute_cycles = []
    # print(nodes)
    max_start = max(start for (start, *_) in cycles.values())
    for node in sorted(cycles.keys(), key=lambda k: cycles[k][1], reverse=True):
        # print(node)
        loop_start, loop_length, end_at = cycles[node]
        relative_ends = set()
        for i in range(loop_length):
            n = max_start + i
            for end in end_at:
                if (end - max_start) % loop_length == n - max_start:
                    relative_ends.add(i)
        compute_cycles.append((max_start, loop_length, sorted(relative_ends)))

    def alligns(n, s1, l1, ends_1):
        for e1 in ends_1:
            if (n - s1 - e1) % l1 == 0:
                return True
        return False

    # Use longest cycle for testing
    start, length, ends = compute_cycles[0]

    print([len(ends) for (_, _, ends) in cycles.values()])
    # print(cycles)
    # print(start, length, ends)
    for i in count():
        # print(i)
        n0 = start + i * length
        for dn in ends:
            n = n0 + dn
            for s1, l1, ends_1 in compute_cycles[1:]:
                if not alligns(n, s1, l1, ends_1):
                    break
            else:
                return n


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
