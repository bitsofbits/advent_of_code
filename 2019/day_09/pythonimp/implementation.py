def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    """
    return [int(x) for x in text.strip().split(',')]


def get_value(x, mode, program, relative_base):
    match mode:
        case 0:
            assert x >= 0
            return program.get(x, 0)
        case 1:
            return x
        case 2:
            assert x + relative_base >= 0
            return program.get(x + relative_base, 0)
        case _:
            raise ValueError(mode)


def set_value(x, v, mode, program, relative_base):
    # TODO: x -> pc, then reg
    x = program[x]
    match mode:
        case 0:
            assert x >= 0
            program[x] = v
        case 2:
            assert x + relative_base >= 0
            program[x + relative_base] = v
        case _:
            raise ValueError(mode)


def get_mode(x, i):
    return (x // 10**i) % 10


def build_computer(program, input_values=None):
    program = {i: x for (i, x) in enumerate(program)}
    relative_base = 0
    pc = 0

    def get(x, i):
        return get_value(x, get_mode(mode, i), program, relative_base)

    def set(x, v, i):
        set_value(x, v, get_mode(mode, i), program, relative_base)

    while True:
        opcode = program[pc] % 100
        mode = program[pc] // 100
        match opcode:
            case 1:  # add
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                set(pc + 3, a + b, 2)
                # assert get_mode(mode, 2) != 1
                # reg = program[pc + 3]
                # program[reg] = a + b
                pc += 4
            case 2:  # multiply
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                set(pc + 3, a * b, 2)
                # assert get_mode(mode, 2) != 1
                # reg = program[pc + 3]
                # program[reg] = a * b
                pc += 4
            case 3:  # input
                # assert get_mode(mode, 0) != 1
                # reg = program[pc + 1]
                v = yield 'thanks for the input'
                set(pc + 1, v, 0)
                pc += 2

            case 4:  # output
                yield get(program[pc + 1], 0)
                pc += 2
            case 5:  # jump-if-true
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                if a:
                    pc = b
                else:
                    pc += 3
            case 6:  # jump-if-false
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                if not a:
                    pc = b
                else:
                    pc += 3
            case 7:  # less-than
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                # assert get_mode(mode, 2) != 1
                # reg = program[pc + 3]
                # program[reg] = a < b
                set(pc + 3, a < b, 2)
                pc += 4
            case 8:  # equal-to
                a = get(program[pc + 1], 0)
                b = get(program[pc + 2], 1)
                # assert get_mode(mode, 2) != 1
                # reg = program[pc + 3]
                # program[reg] = a == b
                set(pc + 3, a == b, 2)
                pc += 4
            case 9:  # adjust relative base
                a = get(program[pc + 1], 0)
                relative_base += a
                pc += 2
            case 99:  # exit
                break
            case _:
                raise ValueError('magic smoke')


def run_computer(program, inputs):
    computer = build_computer(program)
    for x in inputs:
        print(x)
        assert next(computer) == "thanks for the input"
        yield computer.send(x)
    yield from computer


def part_1(text, inputs=[1]):
    """
    >>> part_1(EXAMPLE_TEXT, ())
    [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    >>> part_1('1102,34915192,34915192,7,4,7,99,0', ())
    [1219070632396864]
    >>> part_1('104,1125899906842624,99', ())
    [1125899906842624]

    203 is too low
    """
    program = parse(text)
    return list(run_computer(program, inputs))


def part_2(text, inputs=[2]):
    program = parse(text)
    return list(run_computer(program, inputs))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
