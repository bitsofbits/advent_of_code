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


def render(in_tractor_beam):
    i0 = j0 = 1
    i1 = len(in_tractor_beam) - 1
    j1 = max(x[-1] if x else 0 for x in in_tractor_beam)

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            if j in in_tractor_beam[i]:
                chars.append('#')
            else:
                chars.append('.')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


# A, B, C, D is ground 1, 2, 3, 4 away
# AND X Y sets Y to true if both X and Y are true; otherwise, it sets Y to false.
# OR X Y sets Y to true if at least one of X or Y is true; otherwise, it sets Y to false.
# NOT X Y sets Y to true if X is false; otherwise, it sets Y to false.

# Want to jump if there is a gap at 1, 2, or 3 but not 4

PROGRAM_1 = """\
OR A T
AND B T
AND C T
NOT T T
AND D T
OR T J
WALK
"""


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    19362822
    """
    computer = Computer(parse(text))
    prompt = computer.pop_string()
    assert prompt == "Input instructions:\n"
    instance = computer.copy()
    instance.push_string(PROGRAM_1)
    instance.pop_line()
    instance.pop_line()
    instance.pop_line()
    return instance.pop_output()


def get_subsets(items: str):
    if not items:
        yield ''
    else:
        for x in get_subsets(items[1:]):
            yield items[:1] + x
            yield x


# def _build_programs(length):
#     if length == 0:
#         yield []
#     else:
#         for x in _build_programs(length - 1):
#             yield x
#             for inst in ('OR', 'AND', 'NOT'):
#                 for reg in 'ABCDEFG':
#                     yield x + [f'{inst} {reg} T']


# def build_programs():
#     for program in _build_programs(13):
#         for last_inst in ['OR', 'NOT']:
#             program = program.copy()
#             program.append(f'{last_inst} T J')
#             program.append('RUN')
#             assert len(program) <= 15
#             yield '\n'.join(program) + '\n'
#     *
# _ABCDEFGHI

# !(!D | !(E|I) | !(F|H|I))
#  (D & (E|H) & (F|H|I))
# D & (E & (F|I)) | H)

PROGRAM_2 = """
OR A T
AND B T
AND C T  
NOT T T # !A|!B|!C -> there's an upcoming hole
AND D T # Landing zone clear
OR E J
OR H J  # And we won't be forced to jump into a hole next time
AND J T
NOT T T
NOT T J
RUN
"""


def strip_comments(program):
    lines = []
    for line in program.strip().split('\n'):
        line = line.split('#')[0].strip()
        if line:
            lines.append(line)
    return '\n'.join(lines) + '\n'


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    1143625214
    """
    computer = Computer(parse(text))
    prompt = computer.pop_string()
    assert prompt == "Input instructions:\n"
    instance = computer.copy()
    instance.push_string(strip_comments(PROGRAM_2))
    instance.pop_line()
    instance.pop_line()
    instance.pop_line()
    return_val = instance.pop_output()
    if return_val > 255:
        return return_val
    else:
        failure = (chr(return_val) + instance.pop_string()).strip().split('\n\n')
        print(failure[1])
        print()
        print(failure[-1])


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
