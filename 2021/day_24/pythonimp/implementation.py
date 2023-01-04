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
                    # Value.add(self.reg[a], self.reg.get(b, b))
                case "mul", a, b:
                    if b == 0:
                        self.reg[a] = 0
                    else:
                        self.reg[a] *= self.reg.get(b, b)
                    # Value.mul(self.reg[a], self.reg.get(b, b))
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


def run_subprogram(program, z_values):
    alu = ALU()
    for w in range(1, 10):
        for z in z_values:
            alu.reset({"w": None, "x": None, "y": None, "z": z})
            alu.run(program, [w])
            yield ((w, z), alu.reg["z"])


def find_key(subprog):
    vals = []
    divs = []
    for inst in subprog:
        match inst:
            case "add", "x", int(k):
                vals.append(k)
            case "div", "z", int(k):
                divs.append(k)
    [val] = vals
    [div] = divs
    return val, div


# z -> z + f(v, z % 26) * z
# z % 26 - 6 %= w


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    """
    full_program = parse(text)
    subprograms = list(split_into_subprograms(full_program))
    print(find_key(subprograms[-1]))  # -> -6, 26
    # ->
    z_values = [0]
    omaps = []
    keys = []
    for i, prog in enumerate(subprograms):
        keys.append(find_key(prog))
        om = dict(run_subprogram(prog, z_values))
        omaps.append(om)
        z_values = set(z for (_, z) in om.items() if abs(z) < 26**4)
        # print(z_values)
        # print(i, len(om), len(z_values))

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
        print(d, z)
        digits.append(d)

    print(digits)
    print("".join(str(x) for x in digits))

    z = 0
    digits = []
    for om in z_cands:
        d, z = min((d, z_) for ((d, z0), z_) in om.items() if z0 == z)
        print(d, z)
        digits.append(d)

    print(digits)
    print("".join(str(x) for x in digits))

    # print(z_cands)
    # vals = []
    # for om in omaps:
    #     best = max(z_cands)[0]
    #     vals.append(best)
    #     z_set = [z for (v, z) in v == best]
    #     z_cands = [k for k in om.items() if k]
    # z_values = list(range(-1000, 1001))
    # om = list(run_subprogram(subprograms[-1], z_values))
    # # print([x for x in om if x[-1] == 0])
    # allowed = set([x[0][1] for x in om if x[-1] == 0])
    # print(sorted(allowed))

    # z_values = list(range(-1000, 1001))
    # om = list(run_subprogram(subprograms[-2], z_values))

    # # print([x for x in om if x[-1] == 0])
    # print(set([x[0][1] for x in om if x[-1] in allowed]))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open("../data/input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
