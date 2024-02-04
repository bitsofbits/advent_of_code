def parse_code(text):
    opcode, *rest = (x.strip() for x in text.split())
    return (opcode,) + tuple(int(x) for x in rest)


def parse(text):
    """
    >>> code = parse(EXAMPLE_TEXT)
    >>> code[:2]
    [('#ip', 0), ('seti', 5, 0, 1)]
    """
    return [parse_code(x) for x in text.strip().split('\n')]


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


def run(code, ip_reg, ip=0, reg_2=0):
    registers = [0] * 6
    registers[2] = reg_2
    while True:
        if not 0 <= ip < len(code):
            break
        registers[ip_reg] = ip
        apply(*code[ip], registers)
        ip = registers[ip_reg] + 1
    return registers


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    6
    """
    code = parse(text)
    ip_command, ip_reg = code[0]
    assert ip_command == '#ip'
    code = code[1:]
    registers = run(code, ip_reg)
    return registers[0]


def run2(code, ip_reg):
    ip = 0
    registers = [1] + [0] * 5
    # skipped = False
    while True:
        if not 0 <= ip < len(code):
            break
        if ip == 1:
            break
        registers[ip_reg] = ip
        if ip == 9:
            print(registers)
        apply(*code[ip], registers)
        ip = registers[ip_reg] + 1
    return registers


# Need to hand decode this :-()
def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    15827082
    """
    code = parse(text)
    ip_command, ip_reg = code[0]
    assert ip_command == '#ip'
    code = code[1:]
    registers = run2(code, ip_reg)
    assert 2 * 5275693 == registers[2]
    return sum([1, 10551386, 2, 5275693])


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
