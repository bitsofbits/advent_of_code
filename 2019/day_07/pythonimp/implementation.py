from collections import deque
from itertools import permutations


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:5]
    [3, 15, 3, 16, 1002]
    """
    return [int(x) for x in text.strip().split(',')]


def get_value(x, mode, program):
    return x if mode else program[x]


def get_mode(x, i):
    return (x // 10**i) % 10


def build_amp(program, input_values=None):
    program = {i: x for (i, x) in enumerate(program)}
    pc = 0

    def value(x, i):
        return get_value(x, get_mode(mode, i), program)

    while True:
        opcode = program[pc] % 100
        mode = program[pc] // 100
        match opcode:
            case 1:  # add
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a + b
                pc += 4
            case 2:  # multiply
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a * b
                pc += 4
            case 3:  # input
                assert not get_mode(mode, 0)
                reg = program[pc + 1]
                program[reg] = yield 'thanks for the input'
                pc += 2
            case 4:  # output
                yield value(program[pc + 1], 0)
                pc += 2
            case 5:  # jump-if-true
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                if a:
                    pc = b
                else:
                    pc += 3
            case 6:  # jump-if-false
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                if not a:
                    pc = b
                else:
                    pc += 3
            case 7:  # less-than
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a < b
                pc += 4
            case 8:  # equal-to
                a = value(program[pc + 1], 0)
                b = value(program[pc + 2], 1)
                assert not get_mode(mode, 2)
                reg = program[pc + 3]
                program[reg] = a == b
                pc += 4
            case 99:  # exit
                break
            case _:
                raise ValueError('magic smoke')


def amplify(program, phase_control_values):
    """
    >>> program = parse(EXAMPLE_TEXT)
    >>> amplify(program, [4,3,2,1,0])
    43210

    """
    input_signal = 0
    for phase_control in phase_control_values:
        amp = build_amp(program)
        next(amp)
        amp.send(phase_control)
        input_signal = amp.send(input_signal)
    return input_signal


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    43210
    >>> part_1(EXAMPLE2_TEXT)
    54321
    >>> part_1(EXAMPLE3_TEXT)
    65210
    """
    program = parse(text)
    return max(amplify(program, x) for x in permutations([0, 1, 2, 3, 4]))


def feedback_amplify(program, phase_control_values):
    """
    >>> program = parse(EXAMPLE4_TEXT)
    >>> feedback_amplify(program, [9,8,7,6,5])
    139629729
    >>> program = parse(EXAMPLE5_TEXT)
    >>> feedback_amplify(program, [9,7,8,5,6])
    18216
    """

    amplifiers = []
    for phase_control in phase_control_values:
        amp = build_amp(program.copy())
        next(amp)
        amp.send(phase_control)  # thanks for the input
        amplifiers.append(amp)

    input_signal = 0
    running = True
    while running:
        for amp in amplifiers:
            input_signal = amp.send(input_signal)
            try:
                next(amp)
            except StopIteration:
                running = False
    return input_signal


def part_2(text):
    """
    >>> part_2(EXAMPLE4_TEXT)
    139629729
    >>> part_2(EXAMPLE5_TEXT)
    18216
    """
    program = parse(text)
    return max(feedback_amplify(program, x) for x in permutations([5, 6, 7, 8, 9]))


if __name__ == "__main__":
    import doctest

    EXAMPLE_TEXT = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    EXAMPLE2_TEXT = (
        "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    )
    EXAMPLE3_TEXT = (
        "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
        "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    )
    EXAMPLE4_TEXT = (
        "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
        "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    )
    EXAMPLE5_TEXT = (
        "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
        "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
        "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    )

    doctest.testmod()
