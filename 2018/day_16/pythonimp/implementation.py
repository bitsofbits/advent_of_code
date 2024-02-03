def parse_example(text):
    before, command, after = text.split('\n')
    before = tuple(
        int(x.strip()) for x in before.split(':')[1].strip()[1:-1].split(',')
    )
    command = tuple(int(x.strip()) for x in command.split())
    after = tuple(int(x.strip()) for x in after.split(':')[1].strip()[1:-1].split(','))
    return before, command, after


def parse_code(text):
    return tuple(int(x.strip()) for x in text.split())


def parse(text):
    """
    >>> examples, code = parse(INPUT_TEXT)
    >>> examples[0]
    ((1, 3, 1, 3), (14, 0, 3, 0), (0, 3, 1, 3))
    >>> code[0]
    (9, 2, 0, 0)
    """
    examples, code = text.strip().split("\n\n\n")
    examples = [parse_example(x) for x in examples.strip().split('\n\n')]
    code = [parse_code(x) for x in code.strip().split('\n')]
    return examples, code


opcodes = [
    'addr',
    'addi',
    'mulr',
    'muli',
    'banr',
    'bani',
    'borr',
    'bori',
    'setr',
    'seti',
    'gtir',
    'gtri',
    'gtrr',
    'eqir',
    'eqri',
    'eqrr',
]


def apply(opcode, A, B, C, registers):
    match opcode:
        case 'addr':
            registers[C] = registers[A] + registers[B]
        case 'addi':
            registers[C] = registers[A] + B
        case 'mulr':
            registers[C] = registers[A] * registers[B]
        case 'muli':
            registers[C] = registers[A] * B
        case 'banr':
            registers[C] = registers[A] & registers[B]
        case 'bani':
            registers[C] = registers[A] & B
        case 'borr':
            registers[C] = registers[A] | registers[B]
        case 'bori':
            registers[C] = registers[A] | B
        case 'setr':
            registers[C] = registers[A]
        case 'seti':
            registers[C] = A
        case 'gtir':
            registers[C] = int(A > registers[B])
        case 'gtri':
            registers[C] = int(registers[A] > B)
        case 'gtrr':
            registers[C] = int(registers[A] > registers[B])
        case 'eqir':
            registers[C] = int(A == registers[B])
        case 'eqri':
            registers[C] = int(registers[A] == B)
        case 'eqrr':
            registers[C] = int(registers[A] == registers[B])
        case _:
            raise ValueError(opcode)


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    607
    """
    examples, code = parse(INPUT_TEXT)
    matches = []
    for before, command, after in examples:
        _, A, B, C = command
        count = 0
        for opcode in opcodes:
            registers = list(before)
            apply(opcode, A, B, C, registers)
            if tuple(registers) == after:
                count += 1
        matches.append(count)
    return sum(x >= 3 for x in matches)


def match_opcodes(examples):
    numcodes = {command[0] for (_, command, _) in examples}
    possible = {k: set(opcodes) for k in numcodes}
    for before, command, after in examples:
        numcode, A, B, C = command
        for opcode in opcodes:
            registers = list(before)
            apply(opcode, A, B, C, registers)
            if tuple(registers) != after:
                possible[numcode].discard(opcode)
    opcode_map = {}
    while possible:
        for k, v in possible.items():
            if len(v) == 1:
                break
        [v] = v
        opcode_map[k] = v
        for v1 in possible.values():
            v1.discard(v)
        possible = {k: v for (k, v) in possible.items() if v}
    return opcode_map


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    """
    examples, code = parse(INPUT_TEXT)
    opcode_map = match_opcodes(examples)
    registers = [0, 0, 0, 0]
    for numcode, A, B, C in code:
        apply(opcode_map[numcode], A, B, C, registers)
    return registers[0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
