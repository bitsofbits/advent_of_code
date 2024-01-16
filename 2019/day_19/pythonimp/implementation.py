from collections import defaultdict, deque
from copy import deepcopy
from heapq import heapify, heappop, heappush


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

    def push_all_inputs(self, sequence):
        for x in sequence:
            self.inputs.appendleft(x)
        self.run()

    def pop_output(self):
        return self.outputs.pop()

    def pop_all_outputs(self):
        while self.outputs:
            yield self.outputs.pop()

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


def is_pulled_on(i, j, computer):
    if i < 0 or j < 0:
        return False
    clone = computer.copy()
    clone.push_all_inputs([j, i])
    return bool(clone.pop_output())


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    223
    """
    computer = Computer(parse(text))
    in_tractor_beam = set()
    seen = set()
    queue = [(i, j) for i in range(5) for j in range(5)]
    heapify(queue)
    while queue:
        i, j = heappop(queue)
        if (i, j) in seen or i >= 50 or j >= 50:
            continue
        seen.add((i, j))
        if is_pulled_on(i, j, computer):
            in_tractor_beam.add((i, j))
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    heappush(queue, (i + di, j + dj))
    return len(in_tractor_beam)


def can_fit_square(region, size):
    n_i = len(region)
    for i in range(n_i - size):
        row = region[i]
        if len(row) < size:
            continue
        cumlow = row[0]
        cumhigh = row[-1]
        if len(row) != cumhigh - cumlow + 1:
            continue

        for i1 in range(i + 1, i + size):
            row = region[i1]
            low = row[0]
            high = row[-1]
            if len(row) != high - low + 1:
                break
            cumhigh = min(high, cumhigh)
            cumlow = max(low, cumlow)
            if cumhigh - cumlow + 1 < size:
                break
        else:
            return i, cumlow


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


# TODO
def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    223
    """
    computer = Computer(parse(text))
    in_tractor_beam = [[]]
    seen = set()
    queue = [(i, j) for i in range(5) for j in range(5)]
    heapify(queue)
    last_i = -1
    while queue:
        i, j = heappop(queue)
        if (i, j) in seen:
            continue
        seen.add((i, j))
        if is_pulled_on(i, j, computer):
            if last_i != i:
                if i % 100 == 0:
                    print('.')
                    size = 100
                    if location := can_fit_square(in_tractor_beam, size):
                        y, x = location
                        # print(render(in_tractor_beam, y, x, size))
                        return x * 10000 + y
                last_i = i
            while len(in_tractor_beam) <= i:
                in_tractor_beam.append([])
            heappush(in_tractor_beam[i], j)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    heappush(queue, (i + di, j + dj))
    return sum(len(x) for x in in_tractor_beam.values())


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
