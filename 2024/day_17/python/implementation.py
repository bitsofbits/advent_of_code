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


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    '4,6,3,5,6,3,5,2,1,0'
    """
    registers, program = parse(text)
    computer = Computer(registers)
    output = []
    for x in computer.run(program):
        output.append(str(x))
    return ','.join(output)


def fast(i):
    A = i
    B = C = 0
    while True:
        # if B > 0 or C > 0:
        #     print(i, A, B, C)
        B = A % 8
        B = B ^ 5
        C = A >> B
        B = B ^ 6
        A = A >> 3
        B = B ^ C
        yield B % 8
        if A == 0:
            break



# def part_2(text):
#     """
#     >>> part_2(DATA_TEXT)
#     117440

#     WHILE TRUE:
#         BST REG:A  # B = A % 8
#         BXL 5      # B = B ^ 5 
#         CDV REG:B  # C = A >> B
#         BXL 6      # B = B ^ 6
#         ADV REG:3  # A = A >> 3
#         BXC 2      # B = B ^ C
#         OUT REG:B  # OUTPUT B % 8
#         JNZ 0      # IF A == 0: break

#     WHILE TRUE:
#         BST REG:A  # B = A % 8
#         BXL 5      # B = B ^ 5 
#         CDV REG:B  # C = A >> B
#         ADV REG:3  # A = A >> 3
#         OUT REG:B  # OUTPUT (B ^ C ^ 6) % 8
#         JNZ 0      # IF A == 0: break
#     """
#     registers, program = parse(text)
#     for i in count():
#         if i % 1_000_000 == 0:
#             print(i)
#         try:
#             for a, b in zip(program, fast(i), strict=True):
#                 if a != b:
#                     continue
#             else:
#                 return i
#         except ValueError:
#             pass


def part_2(text):
    """
    >>> part_2(DATA_TEXT)
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

    WHILE TRUE:
        BST REG:A  # B = A % 8
        BXL 5      # B = B ^ 5 
        CDV REG:B  # C = A >> B
        ADV REG:3  # A = A >> 3
        OUT REG:B  # OUTPUT (B ^ C ^ 6) % 8
        JNZ 0      # IF A == 0: break
    """

    registers, program = parse(text)
    computer = Computer(registers)
    table = {}
    for i in range(8 * 8 * 128):
        computer.registers = registers.copy()
        computer.registers['A'] = i
        try:
            [v] = computer.run_till_halt(program)
        except ValueError:
            continue
        higher_order_bits = (i // 8) % 1024
        key = (higher_order_bits, v)
        lower_order_bits = i % 8
        if key not in table:
            table[key] = []
        table[key].append(lower_order_bits)

    print(table)
    # print([x for x in table if x[1] == 2])

    # higher_order_bits = 0 # only choice for output of 2
    # for code in reversed(program):
    #     key = (higher_order_bits % 1024, code)
    #     print(key)
    #     try:
    #         bits = table[key]
    #     except:
    #         print("no key", bits)
    #         break
    #     higher_order_bits <<= 3
    #     higher_order_bits += bits 
    # print(bits)

    # for i, x in enumerate(table):
    #     if x == program[0]:
    #         print(i % 8)



    # min_a = 1 << (3 * 15)
    # max_a = 1 << (3 * 16) - 1

    # for i in range(min_a, max_a):
    #     for n, x in enumerate(fast(i)):
    #         if n >= len(program) or x != program[n]:
    #             break
    #     else:
    #         print(n)
    #         if n + 1 == len(program):
    #             return i




if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example_2.txt") as f:
        EXAMPLE_2_TEXT = f.read()
    with open(data_dir / "data.txt") as f:
        DATA_TEXT = f.read()
    doctest.testmod()
