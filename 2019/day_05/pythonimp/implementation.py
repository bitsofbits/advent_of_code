def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1002, 4, 3, 4, 33]
    """
    return [int(x) for x in text.strip().split(',')]


def get_value(x, mode, program):
    return x if mode else program[x]


def get_mode(x, i):
    return (x // 10**i) % 10


def compute(program, input_value=None):
    """
    >>> program = parse(EXAMPLE_TEXT)
    >>> compute(program)
    (None, [1002, 4, 3, 4, 99])

    >>> program = parse(EXAMPLE_2_TEXT)
    >>> compute(program.copy(), 7)[0]
    999
    >>> compute(program.copy(), 8)[0]
    1000
    >>> compute(program.copy(), 11)[0]
    1001
    """
    program = {i: x for (i, x) in enumerate(program)}
    pc = 0
    output_value = None

    def value(x, i):
        return get_value(x, get_mode(mode, i), program)

    while True:
        opcode = program[pc] % 100
        mode = program[pc] // 100
        match opcode:
            case 1:  # add
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a + b
                pc += 4
            case 2:  # multiply
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a * b
                pc += 4
            case 3:  # input
                assert not get_mode(mode, 0)
                reg = program[pc + 1]
                program[reg] = input_value
                pc += 2
            case 4:  # output
                output_value = value(program[pc + 1], 0)
                pc += 2
            case 5:  # jump-if-true
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                if a:
                    pc = b
                else:
                    pc += 3
            case 6:  # jump-if-false
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                if not a:
                    pc = b
                else:
                    pc += 3
            case 7:  # less-than
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a < b
                pc += 4
            case 8:  # equal-to
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a == b
                pc += 4
            case 99:  # exit
                break
            case _:
                raise ValueError('magic smoke')
    return output_value, [program.get(i) for i in range(max(program) + 1)]


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    5346030
    """
    output_value, _ = compute(parse(text), 1)
    return output_value


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    513116
    """
    output_value, _ = compute(parse(text), 5)
    return output_value


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example_2.txt") as f:
        EXAMPLE_2_TEXT = f.read()

    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
