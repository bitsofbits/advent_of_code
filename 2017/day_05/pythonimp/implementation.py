def parse(text):
    return [int(x) for x in text.strip().split()]


def execute(jumps):
    pc = 0
    n = len(jumps)
    while 0 <= pc < n:
        next_pc = pc + jumps[pc]
        jumps[pc] += 1
        pc = next_pc
        yield pc


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5
    """
    return sum(1 for _ in execute(parse(text)))


def execute2(jumps):
    pc = 0
    n = len(jumps)
    while 0 <= pc < n:
        next_pc = pc + jumps[pc]
        if jumps[pc] >= 3:
            jumps[pc] -= 1
        else:
            jumps[pc] += 1
        pc = next_pc
        yield pc


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    10
    """
    return sum(1 for _ in execute2(parse(text)))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
