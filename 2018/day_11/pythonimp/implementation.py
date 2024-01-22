def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    8
    """
    return int(text.strip())


# Find the fuel cell's rack ID, which is its X coordinate plus 10.
# Begin with a power level of the rack ID times the Y coordinate.
# Increase the power level by the value of the grid serial number (your puzzle input).
# Set the power level to itself multiplied by the rack ID.
# Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
# Subtract 5 from the power level.


def power_level(x, y, sn):
    """
    >>> sn = parse(EXAMPLE_TEXT)
    >>> power_level(3, 5, sn)
    4
    """
    rack_id = x + 10
    power_level = rack_id * y
    power_level += sn
    power_level *= rack_id
    power_level = (power_level // 100) % 10
    return power_level - 5


def blockify_x(target, powers, y, size):
    current_block = sum(powers[x, y] for x in range(1, size + 1))
    target[(1, y)] = current_block
    for x in range(2, 300 + 1 - size):
        current_block = current_block - powers[x - 1, y] + powers[x + size - 1, y]
        target[x, y] = current_block


def blockify_y(target, x_blocked, x, size):
    current_block = sum(x_blocked[x, y] for y in range(1, size + 1))
    target[(x, 1)] = current_block
    for y in range(2, 300 + 1 - size):
        current_block = current_block - x_blocked[x, y - 1] + x_blocked[x, y + size - 1]
        target[x, y] = current_block


def blockify(powers, size):
    x_blocked = {}
    for y in range(1, 301):
        blockify_x(x_blocked, powers, y, size)

    blocked = {}
    for x in range(1, 301 - size):
        blockify_y(blocked, x_blocked, x, size)

    return blocked


def part_1(text):
    """
    >>> part_1('18')
    (33, 45)
    """
    serial_number = parse(text)
    powers = {}
    for x in range(1, 301):
        for y in range(1, 301):
            powers[x, y] = power_level(x, y, serial_number)

    blocked = blockify(powers, 3)
    return max(blocked, key=lambda x: blocked[x])


def part_2(text):
    """
    >>> part_2("18")
    (90, 269, 16)
    """
    serial_number = parse(text)
    powers = {}
    for x in range(1, 301):
        for y in range(1, 301):
            powers[x, y] = power_level(x, y, serial_number)

    max_power = 0
    best_config = None
    for size in range(1, 300):
        blocked = blockify(powers, size)
        xy = max(blocked, key=lambda x: blocked[x])
        if blocked[xy] > max_power:
            max_power = blocked[xy]
            best_config = xy + (size,)
    return best_config


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
