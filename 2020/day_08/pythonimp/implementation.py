def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('nop', 0)
    ('acc', 1)
    ('jmp', 4)
    ('acc', 3)
    ('jmp', -3)
    ('acc', -99)
    ('acc', 1)
    ('jmp', -4)
    ('acc', 6)
    """
    for line in text.strip().split("\n"):
        cmd, arg = line.strip().split()
        yield cmd, int(arg)


def execute(code):
    code = list(code)
    N = len(code)
    acc = 0
    pc = 0
    visited = set()
    while pc not in visited and 0 <= pc < N:
        visited.add(pc)
        match code[pc]:
            case "nop", _:
                pass
            case "acc", x:
                acc += x
            case "jmp", x:
                pc += x - 1
            case _:
                raise ValueError(code[pc])
        pc += 1
    return acc, (pc in visited)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5
    """
    acc, _ = execute(parse(text))
    return acc


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    8
    """
    code = list(parse(text))
    for i, (cmd, x) in enumerate(code):
        if cmd == "acc":
            continue
        modified = code.copy()
        if cmd == "nop":
            modified[i] = ("jmp", x)
        elif cmd == "jmp":
            modified[i] = ("nop", x)
        acc, stuck = execute(modified)
        if not stuck:
            return acc


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
