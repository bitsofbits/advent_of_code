from collections import defaultdict
from typing import NamedTuple


class Rule(NamedTuple):
    value: int
    move: int
    state: str


def parse_setup(text):
    lines = text.strip().split("\n")
    initial_state = lines[0].split()[-1][:-1]
    steps = int(lines[1].split()[-2])
    return initial_state, steps


def parse_subsect(state, lines):
    value = int(lines[0].split()[-1][:-1])
    next_value = int(lines[1].split()[-1][:-1])
    move = {"left": -1, "right": 1}[lines[2].split()[-1][:-1]]
    next_state = lines[3].split()[-1][:-1]
    k = (state, value)
    return k, Rule(next_value, move, next_state)


def parse_section(text):
    lines = text.strip().split("\n")
    state = lines[0][:-1].split()[-1]
    return parse_subsect(state, lines[1:5]), parse_subsect(state, lines[5:9])


def parse(text):
    """
    >>> setup, rules = parse(EXAMPLE_TEXT)
    >>> print(setup)
    ('A', 6)
    >>> for x in rules.items(): print(x)
    (('A', 0), Rule(value=1, move=1, state='B'))
    (('A', 1), Rule(value=0, move=-1, state='B'))
    (('B', 0), Rule(value=1, move=-1, state='A'))
    (('B', 1), Rule(value=1, move=1, state='A'))
    """
    chunks = text.strip().split("\n\n")
    setup = parse_setup(chunks[0])
    rules = {}
    for x in chunks[1:]:
        rules.update(parse_section(x))
    return setup, rules


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    (state, n_steps), rules = parse(text)
    tape = defaultdict(int)
    cursor = 0
    for _ in range(n_steps):
        r = rules[state, tape[cursor]]
        state = r.state
        tape[cursor] = r.value
        cursor += r.move
    return sum(tape.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
