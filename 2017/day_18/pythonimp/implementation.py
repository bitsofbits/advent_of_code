from collections import defaultdict, deque


def maybe_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('set', 'a', 1)
    ('add', 'a', 2)
    ('mul', 'a', 'a')
    ('mod', 'a', 5)
    ('snd', 'a')
    ('set', 'a', 0)
    ('rcv', 'a')
    ('jgz', 'a', -1)
    ('set', 'a', 1)
    ('jgz', 'a', -2)
    """
    for line in text.strip().split("\n"):
        cmd, *args = line.strip().split()
        yield cmd, *(maybe_int(x) for x in args)


class Tablet:
    def __init__(self, **registers):
        self.reset(**registers)

    def reset(self, **registers):
        self.registers = defaultdict(int)
        self.registers.update(registers)

    def execute(self, code):
        sound = None

        def get(r):
            return r if (isinstance(r, int)) else self.registers[r]

        code = list(code)
        pc = 0
        while 0 <= pc < len(code):
            match code[pc]:
                case "snd", a:
                    sound = get(a)
                case "set", a, b:
                    self.registers[a] = get(b)
                case "add", a, b:
                    self.registers[a] += get(b)
                case "mul", a, b:
                    self.registers[a] *= get(b)
                case "rcv", a:
                    if get(a) != 0:
                        return sound
                case "mod", a, b:
                    self.registers[a] %= get(b)
                case "jgz", a, b:
                    if get(a) > 0:
                        pc += get(b) - 1
                case _:
                    raise ValueError((code[pc]))
            pc += 1


# snd X plays a sound with a frequency equal to the value of X.
# set X Y sets register X to the value of Y.
# add X Y increases register X by the value of Y.
# mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
# mod X Y sets register X to the remainder of dividing the value contained in register X by the value of Y (that is, it sets X to the result of X modulo Y).
# rcv X recovers the frequency of the last sound played, but only when the value of X is not zero. (If it is zero, the command does nothing.)
# jgz X Y jumps with an offset of the value of Y, but only if the value of X is greater than zero. (An offset of 2 skips the next instruction, an offset of -1 jumps to the previous instruction, and so on.)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4
    """
    t = Tablet()
    return t.execute(parse(text))


class Tablet2:
    def __init__(self, identity, code):
        self.pc = 0
        self.output = deque()
        self.registers = defaultdict(int)
        self.identity = identity
        self.registers["p"] = identity
        self.code = list(code)
        self.sent_count = 0

    def execute(self, registers=None):

        if registers is not None:
            self.registers.update(registers)

        def get(r):
            if isinstance(r, int):
                return r
            assert "a" <= r <= "z"
            assert isinstance(self.registers[r], int), self.registers
            return self.registers[r]

        while 0 <= self.pc < len(self.code):

            match self.code[self.pc]:
                case "snd", a:
                    self.sent_count += 1
                    self.output.append(get(a))
                case "set", a, b:
                    self.registers[a] = get(b)
                case "add", a, b:
                    self.registers[a] += get(b)
                case "mul", a, b:
                    self.registers[a] *= get(b)
                case "rcv", a:
                    self.pc += 1
                    return a
                case "mod", a, b:
                    self.registers[a] %= get(b)
                case "jgz", a, b:
                    if get(a) > 0:
                        self.pc += get(b) - 1
                case _:
                    raise ValueError((code[pc]))
            self.pc += 1


EXAMPLE2_TEXT = """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
"""


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    3
    """
    code = list(parse(text))
    tblt_0 = Tablet2(0, code)
    tblt_1 = Tablet2(1, code)
    r0 = tblt_0.execute()
    r1 = tblt_1.execute()
    while True:
        if tblt_1.output:
            r0 = tblt_0.execute({r0: tblt_1.output.popleft()})
        elif tblt_0.output:
            r1 = tblt_1.execute({r1: tblt_0.output.popleft()})
        else:
            return tblt_1.sent_count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
