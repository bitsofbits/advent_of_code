# 10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL

from collections import defaultdict
from math import ceil


def parse_item(item):
    count, name = item.strip().split()
    count = int(count)
    return name, count


def parse_line(line):
    inputs, output = (x.strip() for x in line.split('=>'))
    output_name, n_outputs = parse_item(output)
    inputs = [parse_item(x) for x in inputs.split(',')]
    return output_name, n_outputs, inputs


def parse(text):
    """
    >>> reactions = parse(EXAMPLE_TEXT)
    """
    reactions = {}
    for line in text.strip().split('\n'):
        output_name, n_outputs, inputs = parse_line(line)
        reactions[output_name] = (n_outputs, frozenset(inputs))
    return reactions


def ore_needed(n_fuel, reactions):
    pending = [(n_fuel, "FUEL")]
    ore_needed = 0
    inventory = defaultdict(int)
    while pending:
        output_needed, output_name = pending.pop()

        if output_name == 'ORE':
            ore_needed += output_needed
            continue

        inventory_used = min(inventory[output_name], output_needed)
        output_needed -= inventory_used
        inventory[output_name] -= inventory_used

        if output_needed > 0:
            n_outputs, inputs = reactions[output_name]
            n_reactions = ceil(output_needed / n_outputs)
            inventory[output_name] += n_reactions * n_outputs - output_needed

            for input_name, n_inputs in inputs:
                next_count = n_reactions * n_inputs
                pending.append((next_count, input_name))

    return ore_needed


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    31
    >>> part_1(EXAMPLE2_TEXT)
    13312
    >>> part_1(EXAMPLE3_TEXT)
    2210736
    """
    reactions = parse(text)
    return ore_needed(n_fuel=1, reactions=reactions)


def part_2(
    text,
):
    """
    >>> part_2(EXAMPLE2_TEXT)
    82892753
    >>> part_2(EXAMPLE3_TEXT)
    460664
    """
    reactions = parse(text)
    n_ore = 1_000_000_000_000
    low = 0
    high = n_ore
    while low < high - 1:
        n_fuel = (low + high) // 2
        if ore_needed(n_fuel, reactions=reactions) > n_ore:
            high = n_fuel
        else:
            low = n_fuel
    return low


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
