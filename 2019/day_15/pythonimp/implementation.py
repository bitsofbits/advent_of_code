from collections import deque
from copy import deepcopy
from heapq import heappop, heappush
from math import inf


def parse(text):
    return [int(x) for x in text.strip().split(',')]


def sign(x):
    return int(x > 0) - int(x < 0)


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

    def pop_output(self):
        return self.outputs.pop()

    def pop_all_output(self):
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


delta_ij = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}


def traverse(computer):
    queue = [(0, (0, 0), 1, computer)]
    visited = set()
    walls = set()
    best_count = inf
    generator_loc = None
    while queue:
        count, point, status, computer = heappop(queue)

        if point in visited or point in walls:
            continue

        assert status in (0, 1, 2)
        if status == 0:
            walls.add(point)
            continue
        elif status == 1:
            visited.add(point)
        elif status == 2:
            best_count = min(best_count, count)
            assert generator_loc is None
            generator_loc = point
            # Don't just return here because we want to make sure to fill full map
            continue

        for command in (1, 2, 3, 4):
            next_computer = computer.copy()
            next_computer.push_input(command)
            next_status = next_computer.pop_output()
            next_count = count + 1
            di, dj = delta_ij[command]
            i0, j0 = point
            next_point = (i0 + di, j0 + dj)
            heappush(queue, (next_count, next_point, next_status, next_computer))
    return best_count, generator_loc, walls


def render(walls):
    i0 = min(i for (i, j) in walls)
    i1 = max(i for (i, j) in walls)
    j0 = min(j for (i, j) in walls)
    j1 = max(j for (i, j) in walls)

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            if (i, j) in walls:
                chars.append('#')
            else:
                chars.append('.')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def part_1(text, return_maze=False):
    """
    >>> part_1(INPUT_TEXT, return_maze=True)
    404

    """
    computer = Computer(parse(text))
    count, *_ = traverse(computer)
    return count


def fill_from(location, walls):
    queue = [(0, location)]
    visited = set()
    max_time = 0
    while queue:
        time, point = heappop(queue)
        if point in visited or point in walls:
            continue
        visited.add(point)
        max_time = max(time, max_time)

        next_time = time + 1
        i0, j0 = point
        for di, dj in delta_ij.values():
            next_point = (i0 + di, j0 + dj)
            queue.append((next_time, next_point))
    return max_time


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    406
    """
    computer = Computer(parse(text))
    best_count, generator_loc, walls = traverse(computer)
    return fill_from(generator_loc, walls)
    # TODO: flood fill and count iterations


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
