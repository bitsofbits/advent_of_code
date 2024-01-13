from collections import deque


def sign(x):
    return int(x > 0) - int(x < 0)


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


def render(board):
    i0 = min(i for (i, j) in board)
    i1 = max(i for (i, j) in board)
    j0 = min(j for (i, j) in board)
    j1 = max(j for (i, j) in board)

    # 0 is an empty tile. No game object appears in this tile.
    # 1 is a wall tile. Walls are indestructible barriers.
    # 2 is a block tile. Blocks can be broken by the ball.
    # 3 is a horizontal paddle tile. The paddle is indestructible.
    # 4 is a ball tile. The ball moves diagonally and bounces off objects.

    scan_lines = []
    for i in range(i0, i1 + 1):
        chars = []
        for j in range(j0, j1 + 1):
            match board.get((i, j), 0):
                case 0:
                    chars.append(' ')
                case 1:
                    chars.append('#')
                case 2:
                    chars.append('*')
                case 3:
                    chars.append('_')
                case 4:
                    chars.append('o')
                case _:
                    raise ValueError()
        scan_lines.append(''.join(chars))
    return '\n'.join(scan_lines)


def batched(p, n):
    accum = []
    for x in p:
        accum.append(x)
        if len(accum) == n:
            yield tuple(accum)
            del accum[:]
    if accum:
        yield tuple(accum)


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    298
    """
    program = parse(text)
    computer = Computer(program)
    board = {}
    for j, i, tile_id in batched(computer.pop_all_output(), 3):
        board[i, j] = tile_id
    return sum((x == 2) for x in board.values())
    # print(render(board))


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    13956
    """
    program = parse(text)
    program[0] = 2  # insert quarters
    computer = Computer(program)
    last_x = last_y = None
    delta_x = 1
    delta_y = 1
    paddle_y = paddle_x = None
    board = {}
    max_score = 0
    while not board or 2 in board.values():
        for j, i, tile_id in batched(computer.pop_all_output(), 3):
            if (j, i) == (-1, 0):
                max_score = max(tile_id, max_score)
            else:
                board[i, j] = tile_id
            if tile_id == 3:
                paddle_x, paddle_y = j, i
            if tile_id == 4:
                x, y = j, i
                if last_x is not None:
                    delta_x = x - last_x
                    delta_y = y - last_y
                last_x = x
                last_y = y

        if y > paddle_y:
            break

        if board.get((y + delta_y, x + delta_x), 0) != 0:
            delta_x = delta_y = 0

        dy = paddle_y - y
        computer.push_input(x + delta_x * dy - paddle_x)

    assert 2 not in board.values()
    return max_score


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
