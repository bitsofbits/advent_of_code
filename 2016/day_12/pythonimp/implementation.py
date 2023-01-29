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
            match program[pc]:
                case "cpy", x, y:
                    registers[y] = x if isinstance(x, int) else registers[x]
                case "inc", x:
                    registers[x] += 1
                case "dec", x:
                    registers[x] -= 1
                case "jnz", x, n:
                    if (x if isinstance(x, int) else registers[x]) != 0:
                        pc += n - 1
                case _:
                    raise ValueError(program[pc])
            pc += 1
        assert pc > 0


def maybe_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:-1]
    [('cpy', 41, 'a'), ('inc', 'a'), ('inc', 'a'), ('dec', 'a'), ('jnz', 'a', 2)]
    """
    for line in text.strip().split("\n"):
        yield tuple(maybe_int(x) for x in line.strip().split())


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    42
    """
    comp = Computer()
    comp.execute(parse(text))
    return comp.registers["a"]


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    42
    """
    comp = Computer(c=1)
    comp.execute(parse(text))
    return comp.registers["a"]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
