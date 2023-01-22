def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [('inc', 'a'), ('jio', 'a', 2), ('tpl', 'a'), ('inc', 'a')]
    """
    instructions = []
    for line in text.strip().split("\n"):
        inst, payload = line.strip().split(maxsplit=1)
        payload = payload.split(", ")
        if len(payload) == 1:
            if payload[0] not in "ab":
                payload[0] = int(payload[0])
        else:
            payload[1] = int(payload[1])
        instructions.append((inst, *payload))
    return instructions


def execute(instructions, a=0, b=0):
    """
    >>> execute(parse(EXAMPLE_TEXT))
    {'a': 2, 'b': 0}
    """
    registers = {"a": a, "b": b}
    i = 0
    n = len(instructions)
    while 0 <= i < n:
        match instructions[i]:
            case "hlf", r:
                registers[r] //= 2
            case "tpl", r:
                registers[r] *= 3
            case "inc", r:
                registers[r] += 1
            case "jmp", offset:
                i += offset - 1
            case "jie", r, offset:
                if registers[r] % 2 == 0:
                    i = i - 1 + offset
            case "jio", r, offset:
                if registers[r] == 1:
                    i = i - 1 + offset
            case _:
                raise ValueError(instructions[i])
        i += 1
    return registers


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    0
    """
    return execute(parse(text))["b"]


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    return execute(parse(text), a=1)["b"]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
