from collections import deque
from copy import deepcopy
from functools import cache
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


def find_intersections(image):
    image = image.strip().split('\n')
    m = len(image)
    n = len(image[0])
    for i0 in range(1, m - 1):
        assert len(image[i0]) == n
        for j0 in range(1, n - 1):
            for di, dj in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                i = i0 + di
                j = j0 + dj
                if image[i][j] not in '#^v<>':
                    break
            else:
                yield i0, j0


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    5740
    """
    computer = Computer(parse(text))
    outputs = computer.pop_all_outputs()
    image = ''.join(chr(x) for x in outputs)
    intersections = list(find_intersections(image))
    return sum(a * b for (a, b) in intersections)


def build_state(map):
    scaffold = set()
    robot_state = None
    for i, row in enumerate(map.strip().split('\n')):
        for j, x in enumerate(row):
            if x != '.':
                scaffold.add((i, j))
                if x != '#':
                    robot_state = (i, j, '^>v<'.index(x))
    return scaffold, robot_state


delta_ij = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}


@cache
def next_states(state, is_straight):
    i, j, direction = state
    di, dj = delta_ij[direction]
    if (i, j) in is_straight:
        return [('F', (i + di, j + dj, direction))]
    else:
        return [
            ('F', (i + di, j + dj, direction)),
            ('R', (i, j, (direction + 1) % 4)),
            ('L', (i, j, (direction - 1) % 4)),
        ]


def find_straight(scaffold):
    is_straight = set()
    for i0, j0 in scaffold:
        directions = []
        for direction, (di, dj) in delta_ij.items():
            if (i0 + di, j0 + dj) in scaffold:
                directions.append(direction)
        if len(directions) == 2:
            d1, d2 = directions
            if d1 == (d2 + 2) % 4:
                is_straight.add((i0, j0))
    return frozenset(is_straight)


def traverse(scaffold, robot_state):
    is_straight = find_straight(scaffold)
    queue = [(1, 0, robot_state, frozenset({robot_state[:2]}), ())]
    states = set()
    while queue:
        _, count, state, visited, commands = heappop(queue)
        key = (state, visited)
        if key in states:
            continue
        states.add(key)

        next_count = count if (commands[:-2] == ('F', 'F')) else count + 1
        next_visited = visited | {state[:2]}

        if len(next_visited) == len(scaffold):
            return commands

        for command, next_state in next_states(state, is_straight):
            next_position = next_state[:2]
            if next_position in scaffold:
                next_commands = commands + (command,)
                heappush(
                    queue,
                    (
                        -len(next_visited),
                        next_count,
                        next_state,
                        next_visited,
                        next_commands,
                    ),
                )


def render(scaffold, robot_state, is_straight=(), visited=()):
    i0 = min(i for (i, j) in scaffold)
    i1 = max(i for (i, j) in scaffold)
    j0 = min(j for (i, j) in scaffold)
    j1 = max(j for (i, j) in scaffold)

    (i_r, j_r, d_r) = robot_state

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            if (i, j) == (i_r, j_r):
                chars.append('^>v<'[d_r])
                assert (i, j) in scaffold
            elif (i, j) in scaffold:
                if (i, j) in visited:
                    chars.append('*')
                elif (i, j) in is_straight:
                    chars.append('#')
                else:
                    chars.append('@')
            else:
                chars.append('.')
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def condense_commands(commands):
    forward_count = 0
    for x in commands:
        if x in 'LR':
            if forward_count > 0:
                yield str(forward_count)
                forward_count = 0
            yield x
        else:
            forward_count += 1
    if forward_count > 0:
        yield str(forward_count)


def encode_next(sequence, dictionary):
    for name, run in zip("ABC", dictionary):
        if run == sequence[: len(run)]:
            # Greedy, not general
            return name
    return None


def encode_commands(commands):
    # Find candidates for dictionary. Needs to be at most 20 bytes long including commas
    runs = set()
    n_commands = len(commands)
    for i in range(n_commands):
        for j in range(i + 1, n_commands):
            run = commands[i:j]
            char_count = len(','.join(str(x) for x in run))
            if char_count > 20:
                break
            runs.add(tuple(run))

    runs = sorted(runs)
    commands = tuple(commands)

    for i, A in enumerate(runs):
        for j, B in enumerate(runs[i + 1 :]):
            for C in runs[j + 1 :]:
                remaining_commands = commands
                encoded = []
                while remaining_commands:
                    if name := encode_next(remaining_commands, [A, B, C]):
                        next_run = {'A': A, 'B': B, 'C': C}[name]
                        encoded.append(name)
                        remaining_commands = remaining_commands[len(next_run) :]
                    else:
                        break
                else:
                    if len(encoded) < 20:
                        yield encoded, (A, B, C)


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    1022165
    """
    computer = Computer(parse(text))
    outputs = computer.pop_all_outputs()
    image = ''.join(chr(x) for x in outputs)
    scaffold, robot_state = build_state(image)
    # is_straight = find_straight(scaffold)
    commands = traverse(scaffold, robot_state)
    # print(render(scaffold, robot_state, is_straight))
    commands = list(condense_commands(commands))
    encoded_command_sets = list(encode_commands(commands))
    main, (A, B, C) = encoded_command_sets[0]
    main = ','.join(main) + '\n'
    (A, B, C) = (','.join(x) + '\n' for x in (A, B, C))
    # Reset computer and wake up robot
    program = parse(text)
    program[0] = 2
    computer = Computer(program)
    _ = computer.pop_all_outputs()  # drop initial image
    for line in (main, A, B, C, 'n\n'):
        computer.push_all_inputs(ord(x) for x in line)
    outputs = list(computer.pop_all_outputs())
    dust = outputs[-1]
    image = ''.join(chr(x) for x in outputs[:-1]).strip()
    # print(image)
    return dust


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
