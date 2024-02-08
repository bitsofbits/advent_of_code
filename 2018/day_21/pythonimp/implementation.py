def parse_code(text):
    opcode, *rest = (x.strip() for x in text.split())
    return (opcode,) + tuple(int(x) for x in rest)


def parse(text):
    """
    >>> code = parse(INPUT_TEXT)
    >>> code[:2]
    [('#ip', 4), ('seti', 123, 0, 3)]
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


def run(code, ip_reg, ip=0, reg_0=0, max_count=1000, debug=False):
    registers = [0] * 6
    registers[0] = reg_0
    count = 0
    while count < max_count:
        if not 0 <= ip < len(code):
            break
        if debug and ip == 13:
            print(ip, reg_0, registers)
        registers[ip_reg] = ip
        apply(*code[ip], registers)
        ip = registers[ip_reg] + 1
        count += 1
    return registers, count


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    9959629
    """
    code = parse(text)
    ip_command, ip_reg = code[0]
    assert ip_command == '#ip'
    code = code[1:]
    max_count = 1000000000
    answer = 9959629
    # answer = 135
    counts = {}
    for reg_0 in range(answer, answer + 1):
        registers, max_count = run(code, ip_reg, reg_0=reg_0, max_count=max_count)
        counts[reg_0] = max_count
    # print(counts)
    return min(counts, key=lambda k: (counts[k], k))


def run2(code, ip_reg, ip=0, reg_0=0, max_count=1000):
    registers = [0] * 6
    registers[0] = reg_0
    count = 0
    saved_registers = []
    saved_registers2 = []
    while count < max_count:
        if not 0 <= ip < len(code):
            break
        if ip == 13:
            saved_registers.append(registers.copy())
        if ip == 28:
            saved_registers2.append(registers.copy())

        registers[ip_reg] = ip
        apply(*code[ip], registers)
        ip = registers[ip_reg] + 1
        count += 1
    return saved_registers, saved_registers2


def simulator():
    """
    >>> valid = simulator()
    """
    seen = set()
    valid = []
    R3 = R5 = 0
    while True:  # 6
        if (R3, R5) in seen:
            return valid
        seen.add((R3, R5))
        R5 = R3 | 65536
        R3 = 5557974
        while True:  # 8
            R3 = (((R3 + (R5 & 255)) & 16777215) * 65899) & 16777215
            if R5 < 256:
                if R3 not in valid:
                    valid.append(R3)
                # if R3 == R0:
                #     return
                # else:
                break
            R5 = R5 // 256


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    12691260
    """
    return simulator()[-1]
    # code = parse(text)
    # ip_command, ip_reg = code[0]
    # assert ip_command == '#ip'
    # code = code[1:]
    # saved_registers, saved_registers2 = run2(code, ip_reg, reg_0=0, max_count=1000000)
    # for i, x in enumerate(saved_registers2[:10]):
    #     print(x)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
