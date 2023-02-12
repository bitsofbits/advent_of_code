from collections import defaultdict, deque
from math import sqrt


def maybe_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def parse(text):
    """
    >>> for x in list(parse(EXAMPLE_TEXT))[:4]: print(x)
    ('set', 'b', 79)
    ('set', 'c', 'b')
    ('jnz', 'a', 2)
    ('jnz', 1, 5)
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
        def get(r):
            return r if (isinstance(r, int)) else self.registers[r]

        code = list(code)
        mults = 0
        pc = 0
        while 0 <= pc < len(code):
            match code[pc]:
                case "set", a, b:
                    self.registers[a] = get(b)
                case "sub", a, b:
                    self.registers[a] -= get(b)
                case "mul", a, b:
                    mults += 1
                    self.registers[a] *= get(b)
                case "jnz", a, b:
                    if get(a) != 0:
                        pc += get(b) - 1
                case _:
                    raise ValueError((code[pc]))
            pc += 1
        return mults, self.registers["h"]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5929
    """
    code = parse(text)
    tablet = Tablet()
    mults, _ = tablet.execute(code)
    return mults


def is_prime(x):
    for n in range(2, int(sqrt(x))):
        if x % n == 0:
            return False
    return True


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    907
    """
    # After some painful deciphering, turns out code counts from
    # x = b to c (inclusive) and increments h if x is *not* prime.
    count = 0
    b = 79 * 100 + 100_000
    c = b + 17_000
    for i in range(b, c + 1, 17):
        if not is_prime(i):
            count += 1
    return count


if __name__ == "__main__":

    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
