from collections import deque
from itertools import count


def parse_line(line):
    """
    >>> parse_line("inp w")
    ('inp', 'w')
    >>> parse_line("mod w 1")
    ('mod', 'w', 1)
    >>> parse_line("add x y")
    ('add', 'x', 'y')
    >>> parse_line("mul y 99")
    ('mul', 'y', 99)
    >>> parse_line("eql z 10")
    ('eql', 'z', 10)
    """
    a, b, *c = line.strip().split()
    assert b in "wxyz"
    if a == "inp":
        assert len(c) == 0
        return (a, b)
    [c] = c
    if c not in "wxyz":
        c = int(c)
    assert a in ("add", "mul", "div", "mod", "eql")
    return (a, b, c)


def parse(text):
    """
    >>> len(parse(EXAMPLE_TEXT))
    11
    """
    return [parse_line(x) for x in text.strip().split("\n")]


class ALU:
    """
    >>> inst = parse(EXAMPLE_TEXT)
    >>> alu = ALU()
    >>> alu.run(inst, [14, 0])
    >>> alu.reg
    {'w': 1, 'x': 1, 'y': 1, 'z': 0}
    >>> inst = parse(INPUT_TEXT)
    >>> alu.reset()
    >>> inp = [int(x) for x in "79997391969649"]
    >>> alu.run(inst, inp)
    >>> alu.reg["z"]
    0
    """

    def __init__(self):
        self.reset()

    def reset(self, values=()):
        self.reg = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.reg.update(values)

    def run(self, instructions, inputs):
        inputs = deque(inputs)
        for x in instructions:
            match x:
                case "inp", a:
                    self.reg[a] = inputs.popleft()
                case "add", a, b:
                    self.reg[a] += self.reg.get(b, b)
                case "mul", a, b:
                    if b == 0:
                        self.reg[a] = 0
                    else:
                        self.reg[a] *= self.reg.get(b, b)
                case "div", a, b:
                    self.reg[a] = int(self.reg[a] / self.reg.get(b, b))
                    # Value.div(self.reg[a], self.reg.get(b, b))
                case "mod", a, b:
                    self.reg[a] %= self.reg.get(b, b)
                    # Value.mod(self.reg[a], self.reg.get(b, b))
                case "eql", a, b:
                    self.reg[a] = self.reg[a] == self.reg.get(b, b)
                    # Value.eql(self.reg[a], self.reg.get(b, b))
                case _:
                    raise ValueError(x)


def split_into_subprograms(program):
    i0 = 0
    for i1, inst in enumerate(program):
        op, *_ = inst
        if op == "inp" and i1 > 0:
            yield program[i0:i1]
            i0 = i1
    yield program[i0:]


# inp w
# mul x 0
# add x z
# mod x 26
# div z 1 # a
# add x 14 # b
# eql x w
# eql x 0
# mul y 0
# add y 25
# mul y x
# add y 1
# mul z y
# mul y 0
# add y w
# add y 8 # c
# mul y x
# add z y


def extract_fast_subprogram(prog):
    avals = []
    bvals = []
    cvals = []
    for inst in prog:
        match inst:
            case "div", "z", int(a):
                avals.append(a)
            case "add", "x", int(b):
                bvals.append(b)
            case "add", "y", int(c):
                cvals.append(c)
    [a] = avals
    [b] = bvals
    [_, _, c] = cvals
    return a, b, c


def run_fast_subprogram(program, z_values):
    a, b, c = program
    for w in range(1, 10):
        for z in z_values:
            z0 = z
            x = (z % 26 + b) != w
            z = int(z / a)
            y = 25 * x + 1
            z *= y
            y = (w + c) * x
            z += y
            yield (w, z0), z


def run_subprogram(program, z_values):
    alu = ALU()
    for w in range(1, 10):
        for z in z_values:
            alu.reset({"w": None, "x": None, "y": None, "z": z})
            alu.run(program, [w])
            yield ((w, z), alu.reg["z"])


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    79997391969649
    """
    global z_cands
    full_program = parse(text)
    subprograms = list(split_into_subprograms(full_program))
    # ->
    z_values = [0]
    omaps = []
    for i, prog in enumerate(subprograms):
        fastprog = extract_fast_subprogram(prog)
        om = dict(run_fast_subprogram(fastprog, z_values))
        # om = dict(run_subprogram(prog, z_values))
        omaps.append(om)
        z_values = set(z for (_, z) in om.items() if abs(z) < 26**4)

    z_cands = []
    z_set = {0}
    for om in omaps[::-1]:
        zc = {(d, z0): z for ((d, z0), z) in om.items() if z in z_set}
        z_cands.append(zc)
        z_set = set(z0 for (_, z0) in zc)
    z_cands.reverse()
    z = 0
    digits = []
    for om in z_cands:
        d, z = max((d, z_) for ((d, z0), z_) in om.items() if z0 == z)
        digits.append(d)
    return int("".join(str(x) for x in digits))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    16931171414113
    """
    global z_cands
    z = 0
    digits = []
    for om in z_cands:
        d, z = min((d, z_) for ((d, z0), z_) in om.items() if z0 == z)
        digits.append(d)

    return int("".join(str(x) for x in digits))


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open("../data/input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
