from collections import defaultdict


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): pass
    >>> print(x)
    (('c', 'inc', -20), ('c', '==', 10))
    """
    for line in text.strip().split("\n"):
        name, op, amt, _, reg, comp, val = line.strip().split()
        yield (name, op, int(amt)), (reg, comp, int(val))


def execute(program):
    registers = defaultdict(int)
    maxeverval = 0
    for op, cond in program:
        match cond:
            case r, "<", x:
                if not (registers[r] < x):
                    continue
            case r, "<=", x:
                if not (registers[r] <= x):
                    continue
            case r, ">", x:
                if not (registers[r] > x):
                    continue
            case r, ">=", x:
                if not (registers[r] >= x):
                    continue
            case r, "==", x:
                if not (registers[r] == x):
                    continue
            case r, "!=", x:
                if not (registers[r] != x):
                    continue
            case _:
                raise ValueError(cond)
        match op:
            case r, "inc", x:
                registers[r] += x
            case r, "dec", x:
                registers[r] -= x
            case _:
                raise ValueError(op)
        maxeverval = max(maxeverval, registers[r])


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1
    """
    maxval, _ = execute(parse(text))
    return maxval


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    10
    """
    _, maxeverval = execute(parse(text))
    return maxeverval


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
