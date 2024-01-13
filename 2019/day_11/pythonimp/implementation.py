from collections import defaultdict, deque


def parse(text):
    return [int(x) for x in text.strip().split(',')]


def get_value(x, mode, program, relative_base):
    match mode:
        case 0:
            assert x >= 0
            return program.get(x, 0)
        case 1:
            return x
        case 2:
            assert x + relative_base >= 0
            return program.get(x + relative_base, 0)
        case _:
            raise ValueError(mode)


def set_value(x, v, mode, program, relative_base):
    match mode:
        case 0:
            assert x >= 0
            program[x] = v
        case 2:
            assert x + relative_base >= 0
            program[x + relative_base] = v
        case _:
            raise ValueError(mode)


def get_mode(x, i):
    return (x // 10 ** (i - 1)) % 10


class Computer:
    def __init__(self, program):
        self.relative_base = 0
        self.pc = 0
        self.program = {i: x for (i, x) in enumerate(program)}
        self.is_running = True
        self.inputs = deque()
        self.outputs = deque()
        self.run()

    def _get(self, ndx, mode):
        assert ndx >= 1
        src = self.program[self.pc + ndx]
        return get_value(src, get_mode(mode, ndx), self.program, self.relative_base)

    def _set(self, ndx, value, mode):
        assert ndx >= 1
        dst = self.program[self.pc + ndx]
        set_value(dst, value, get_mode(mode, ndx), self.program, self.relative_base)

    def push_input(self, x):
        self.inputs.appendleft(x)
        self.run()

    def pop_output(self):
        return self.outputs.pop()

    def run(self):
        while self.is_running:
            opcode = self.program[self.pc] % 100
            mode = self.program[self.pc] // 100
            match opcode:
                case 1:  # add
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    self._set(3, a + b, mode)
                    self.pc += 4
                case 2:  # multiply
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    self._set(3, a * b, mode)
                    self.pc += 4
                case 3:  # input
                    if not self.inputs:
                        return  # Stop running till we get more inputs
                    self._set(1, self.inputs.pop(), mode)
                    self.pc += 2
                case 4:  # output
                    v = self._get(1, mode)
                    self.outputs.appendleft(v)
                    self.pc += 2
                case 5:  # jump-if-true
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    if a:
                        self.pc = b
                    else:
                        self.pc += 3
                case 6:  # jump-if-false
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    if not a:
                        self.pc = b
                    else:
                        self.pc += 3
                case 7:  # less-than
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    self._set(3, int(a < b), mode)
                    self.pc += 4
                case 8:  # equal-to
                    a = self._get(1, mode)
                    b = self._get(2, mode)
                    self._set(3, int(a == b), mode)
                    self.pc += 4
                case 9:  # adjust relative base
                    a = self._get(1, mode)
                    self.relative_base += a
                    self.pc += 2
                case 99:  # exit
                    self.is_running = False
                case _:
                    raise ValueError(f'unknown opcode: {opcode}')


def paint(hull, computer):
    direction = 0  # up
    i = 0
    j = 0
    while computer.is_running:
        computer.push_input(hull.get((i, j), 0))
        color = computer.pop_output()
        assert color in (0, 1), color
        turn_right = computer.pop_output()
        assert turn_right in (0, 1), turn_right
        hull[i, j] = color
        direction += 1 if turn_right else -1
        direction = direction % 4
        di = dj = 0
        match direction:
            case 0:
                di = -1
            case 1:
                dj = 1
            case 2:
                di = 1
            case 3:
                dj = -1
            case _:
                raise ValueError()
        i += di
        j += dj
    return hull


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    1951
    """
    program = parse(text)
    computer = Computer(program)
    hull = defaultdict(int)
    hull = paint(hull, computer)
    return len(hull)


def render(hull):
    i0 = min(i for (i, j) in hull)
    i1 = max(i for (i, j) in hull)
    j0 = min(j for (i, j) in hull)
    j1 = max(j for (i, j) in hull)

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            if hull.get((i, j), 0):
                chars.append('#')
            else:
                chars.append(' ')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def part_2(text):
    """
    >>> print(part_2(INPUT_TEXT))
    """
    program = parse(text)
    computer = Computer(program)
    hull = defaultdict(int)
    hull[(0, 0)] = 1
    hull = paint(hull, computer)
    return render(hull)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
