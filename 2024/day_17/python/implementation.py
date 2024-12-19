from itertools import count

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ({'A': 729, 'B': 0, 'C': 0}, (0, 1, 5, 4, 3, 0))
    """
    register_text, instruct_text = text.strip().split('\n\n')

    registers = {}
    for line in register_text.split('\n'):
        _, key, value = line.split()
        key = key[:-1]
        registers[key] = int(value)

    _, instruct_text = instruct_text.split()
    instructions = tuple(int(x) for x in instruct_text.split(','))
    return registers, instructions


class Computer:
    """
    >>> computer = Computer({"C" : 9})
    >>> _ = computer.run_till_halt([2, 6])
    >>> computer.registers
    {'C': 9, 'B': 1}

    >>> computer = Computer({"A" : 10})
    >>> computer.run_till_halt([5,0,5,1,5,4])
    [0, 1, 2]

    >>> computer = Computer({"A" : 2024})
    >>> computer.run_till_halt([0,1,5,4,3,0])
    [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    >>> computer.registers['A']
    0

    >>> computer = Computer({"B" : 29})
    >>> _ = computer.run_till_halt([1,7])
    >>> computer.registers['B']
    26

    >>> computer = Computer({"B" : 2024, "C" : 43690})
    >>> _ = computer.run_till_halt([4,0])
    >>> computer.registers['B']
    44354


    """
    def __init__(self, registers=None):
        self.registers = registers.copy()

    def run(self, program):
        reg = self.registers
        pc = 0
        while pc + 1 < len(program):

            match literal := program[pc + 1]:
                case 0 | 1 | 2 | 3:
                    combo = literal
                case 4:
                    combo = reg['A']
                case 5:
                    combo = reg['B']
                case 6:
                    combo = reg['C']
                case 7:
                    combo = None
                case _:
                    raise ValueError(literal)

            op = program[pc]
            pc += 2

            match op:
                case 0: # adv
                    reg['A'] >>= combo
                case 1: # bxl
                    reg['B'] ^= literal
                case 2: # bst
                    reg['B'] = combo & 0b111
                case 3: # jnz
                    if reg['A'] != 0:
                        pc = literal
                case 4: # bxc
                    # ignores x
                    reg['B'] = reg['B'] ^ reg['C']
                case 5: # out
                    yield combo & 0b111
                case 6: # bdv
                    reg['B'] = reg['A'] >> combo
                case 7: # cdv
                    reg['C'] = reg['A'] >> combo
                case _:
                    raise ValueError()

    def run_till_halt(self, program):
        return list(self.run(program))


def part_1(text, A=None):
    """
    >>> part_1(EXAMPLE_TEXT)
    '4,6,3,5,6,3,5,2,1,0'

    >>> part_1(EXAMPLE_3_TEXT, A=117440)
    '0,3,5,4,3,0'

    >>> part_1(DATA_TEXT, A=106086382266778)
    '2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0'
    """
    registers, program = parse(text)
    if A is not None:
        registers['A'] = A
    computer = Computer(registers)
    output = []
    for x in computer.run(program):
        output.append(str(x))
    return ','.join(output)


# def fast(i):
#     A = i
#     B = C = 0
#     while True:
#         # if B > 0 or C > 0:
#         #     print(i, A, B, C)
#         B = A % 8
#         B = B ^ 5
#         C = A >> B
#         B = B ^ 6
#         A = A >> 3
#         B = B ^ C
#         yield B % 8
#         if A == 0:
#             break



def part_2(text, shift=3):
    """
    # >>> part_2(DATA_TEXT)

    >>> part_2(EXAMPLE_3_TEXT, shift=1)
    117440

    WHILE TRUE:
        BST REG:A  # B = A % 8
        BXL 5      # B = B ^ 5 
        CDV REG:B  # C = A >> B
        BXL 6      # B = B ^ 6
        ADV REG:3  # A = A >> 3
        BXC 2      # B = B ^ C
        OUT REG:B  # OUTPUT B % 8
        JNZ 0      # IF A == 0: break
    """

    registers, program = parse(text)
    computer = Computer(registers)

    # Find possible values for first 10^H^H bits
    # I thought this should be 10, but needs 18 to work?
    base_shift = 18
    states = set()
    for i in range(2 ** base_shift):
        computer.registers = registers.copy()
        computer.registers['A'] = i
        computer.registers['A0'] = i
        value = next(computer.run(program))
        if value == program[0]:
            states.add(frozenset(computer.registers.items()))

    for n, op in enumerate(program[1:]):
        next_states = set()
        for i in range(2 ** shift):
            for state in states:
                state = dict(state)
                assert i << (base_shift - shift) & state['A'] == 0
                state['A'] += i << (base_shift - shift)
                state['A0'] += i << (base_shift + n * shift)
                computer.registers = state
                value = next(computer.run(program))
                if value == op:
                    next_states.add(frozenset(computer.registers.items()))
        states = next_states

    final_states = set()
    for state in states:
        registers = dict(state)
        if registers['A'] == 0:
            final_states.add(state)
        value = next(computer.run(program))

    return min(dict(x)["A0"] for x in final_states)




if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example_2.txt") as f:
        EXAMPLE_2_TEXT = f.read()
    with open(data_dir / "example_3.txt") as f:
        EXAMPLE_3_TEXT = f.read()
    with open(data_dir / "data.txt") as f:
        DATA_TEXT = f.read()
    doctest.testmod()
