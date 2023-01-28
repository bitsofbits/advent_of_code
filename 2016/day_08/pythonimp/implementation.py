from __future__ import annotations

from itertools import count

import numpy as np


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('rect', 3, 2)
    ('rotate', 'column', 1, 1)
    ('rotate', 'row', 0, 4)
    ('rotate', 'column', 1, 1)
    """
    for line in text.strip().split("\n"):
        match line.strip().split():
            case "rect", AxB:
                yield "rect", *(int(x) for x in AxB.split("x"))
            case "rotate", which, AxisEqualsA, "by", b:
                yield "rotate", which, int(AxisEqualsA.split("=")[-1]), int(b)
            case _:
                raise ValueError(line)


def display(text, size):
    screen = np.zeros(size, dtype=int)
    for cmd in parse(text):
        match cmd:
            case "rect", dx, dy:
                screen[:dy, :dx] = 1
            case "rotate", "row", row, n:
                screen[row] = np.roll(screen[row], n)
            case "rotate", "column", col, n:
                screen[:, col] = np.roll(screen[:, col], n)
            case _:
                ValueError(cmd)
    return screen


def part_1(text, size):
    """
    >>> part_1(EXAMPLE_TEXT, (3, 7))
    6
    """
    return display(text, size).sum()


def part_2(text, size):
    """
    >>> print(part_2(EXAMPLE_TEXT, (3, 7)))
    | #  # #|
    |# #    |
    | #     |
    """
    screen = display(text, size)
    lines = []
    for row in screen:
        lines.append("|" + "".join(" #"[i] for i in row) + "|")
    return "\n".join(lines)


def fizz_buzz():
    """
    >>> from itertools import islice
    >>> list(islice(fizz_buzz(), 0, 5))
    ['1', '2', 'fizz', '4', 'buzz']
    >>> list(islice(fizz_buzz(), 9, 15))
    ['buzz', '11', 'fizz', '13', '14', 'fizzbuzz']
    """
    for i in count(1):
        match i % 3, i % 5:
            case 0, 0:
                yield "fizzbuzz"
            case 0, _:
                yield "fizz"
            case _, 0:
                yield "buzz"
            case _:
                yield str(i)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
