from math import factorial


class Computer:
    def __init__(self, **registers):
        self.reset(**registers)

    def reset(self, **registers):
        self.registers = {x: 0 for x in "abcd"}
        self.registers.update(registers)

    def execute(self, program):
        program = list(program)
        pc = 0
        registers = self.registers
        # Could rewrite to use list instead of dict of registers
        # adding cpy_reg cpy_val and jnz_reg jnz_val (later could just be jump)
        while 0 <= pc < len(program):
            try:
                match program[pc]:
                    case "cpy", x, y:
                        registers[y] = x if isinstance(x, int) else registers[x]
                    case "inc", x:
                        registers[x] += 1
                    case "dec", x:
                        registers[x] -= 1
                    case "jnz", x, n:
                        if (x if isinstance(x, int) else registers[x]) != 0:
                            n = n if isinstance(n, int) else registers[n]
                            pc += n - 1
                    case "tgl", n:
                        n = pc + (n if isinstance(n, int) else registers[n])
                        if 0 <= n < len(program):
                            match program[n]:
                                case "inc", a:
                                    program[n] = ("dec", a)
                                case _, a:
                                    program[n] = ("inc", a)
                                case "jnz", a, b:
                                    program[n] = ("cpy", a, b)
                                case _, a, b:
                                    program[n] = ("jnz", a, b)
                    case _:
                        raise RuntimeError(program[pc])
            except TypeError:
                raise

            pc += 1
        assert pc > 0


def maybe_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:-2]
    [('cpy', 2, 'a'), ('tgl', 'a'), ('tgl', 'a'), ('tgl', 'a'), ('cpy', 1, 'a')]
    """
    for line in text.strip().split("\n"):
        yield tuple(maybe_int(x) for x in line.strip().split())


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    comp = Computer(a=7)
    comp.execute(parse(text))
    return comp.registers["a"]


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    479010720
    """
    for i in range(6, 9):
        comp = Computer(a=i)
        comp.execute(parse(text))
        # By *painful* inspection
        assert comp.registers["a"] == factorial(i) + 96 * 95
    return factorial(12) + 96 * 95


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    doctest.testmod()
