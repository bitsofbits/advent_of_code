from collections import deque
from copy import deepcopy


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

    def copy(self):
        return deepcopy(self)

    def __lt__(self, other):
        return False

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

    def push_sequence(self, sequence):
        for x in sequence:
            self.inputs.appendleft(x)
        self.run()

    def push_string(self, string):
        self.push_sequence((ord(x) for x in string))

    def pop_output(self):
        return self.outputs.pop()

    def pop_sequence(self):
        while self.outputs:
            yield self.outputs.pop()

    def pop_line(self):
        chars = []
        while True:
            chars.append((x := self.outputs.pop()))
            if x == 10:
                break
        return ''.join(chr(x) for x in chars)

    def pop_string(self):
        return ''.join(chr(x) for x in self.pop_sequence())

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


dangerous_items = {"escape pod", "molten lava", "infinite loop"}


def part_1(text):
    """

    Correct inventory to get past checkpoint:

    - ornament
    - easter egg
    - hypercube
    - monolith

    """
    computer = Computer(parse(text))
    print(computer.pop_string())
    while True:
        computer.push_string(input() + '\n')
        print(computer.pop_string())


def part_2(text):
    """
    # >>> part_2(INPUT_TEXT)
    """
    items = [
        'planetoid',
        'ornament',
        'easter egg',
        'spool of cat6',
        'fixed point',
        'hypercube',
        'monolith',
    ]
    sets = set()
    for i in range(2**7):
        item = set()
        for j, x in enumerate(items):
            if 1 << j & i:
                item.add(x)
        if item:
            sets.add(frozenset(item))

    too_heavy = [
        {
            'planetoid',
            'ornament',
            'easter egg',
            'spool of cat6',
            'fixed point',
            'hypercube',
            'monolith',
        },
        {
            'easter egg',
            'fixed point',
            'hypercube',
            'monolith',
            'ornament',
            'spool of cat6',
        },
        {'easter egg', 'fixed point', 'hypercube', 'monolith', 'ornament', 'planetoid'},
        {
            'fixed point',
            'spool of cat6',
            'hypercube',
            'planetoid',
            'monolith',
            'ornament',
        },
        {'easter egg', 'monolith', 'planetoid', 'hypercube'},
        {'hypercube', 'spool of cat6', 'planetoid', 'monolith'},
        {'hypercube', 'monolith', 'fixed point', 'spool of cat6'},
        {'spool of cat6', 'hypercube', 'easter egg', 'monolith'},
        {'spool of cat6', 'ornament', 'hypercube', 'monolith'},
    ]

    too_light = [
        {
            'planetoid',
            'ornament',
            'easter egg',
            'spool of cat6',
            'fixed point',
            'hypercube',
        },
        {
            'planetoid',
            'ornament',
            'easter egg',
            'spool of cat6',
            'fixed point',
            'monolith',
        },
    ]

    items = set(items)

    for x in sets.copy():
        for y in too_heavy:
            if y.issubset(x):
                sets.remove(x)
                break
        if x not in sets:
            continue
        for y in too_light:
            missing_y = items - y
            missing_x = items - x
            if missing_y.issubset(missing_x):
                sets.remove(x)
                break

    x = sorted(sets, key=lambda x: len(x))[len(sets) // 2]
    print(repr(set(x)))
    print(len(sets))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
