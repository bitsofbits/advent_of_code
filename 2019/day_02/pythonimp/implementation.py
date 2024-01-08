from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    return [int(x) for x in text.strip().split(',')]



def compute(program):
    """
    >>> program = parse(EXAMPLE_TEXT)
    >>> compute(program)
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    program = {i : x for (i, x) in enumerate(program)}
    pc = 0
    while True:
        # opcode = program[pc]
        match program[pc]:
            case 1:
                a = program[program[pc + 1]]
                b = program[program[pc + 2]]
                reg = program[pc + 3]
                program[reg] = a + b
            case 2:
                a = program[program[pc + 1]]
                b = program[program[pc + 2]]
                reg = program[pc + 3]
                program[reg] = a * b
            case 99:
                break
            case _:
                raise ValueError('magic smoke')
        pc += 4
    return [program.get(i) for i in range(max(program) + 1)]



def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    4138687
    """
    program = parse(text)
    program[1:3] = [12, 2]
    return compute(program)[0]


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    program = parse(text)
    for total in count():
        for noun in range(total + 1):
            verb = total - noun
            program[1:3] = [noun, verb]
            if compute(program)[0] == 19690720:
                return 100 * noun + verb


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()


    doctest.testmod()
