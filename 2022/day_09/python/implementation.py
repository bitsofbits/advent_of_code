"""Implementation of Aoc 2022 day 9

>>> moves = load_moves("data/example1.txt")
>>> find_n_tail_locs(Rope(2), moves)
13
>>> moves = load_moves("data/example2.txt")
>>> find_n_tail_locs(Rope(10), moves)
36


"""
from typing import NamedTuple


def sign(x):
    if x == 0:
        return 0
    return 1 if (x > 0) else -1


class Move(NamedTuple):
    direction: str
    count: int


class Rope:
    def __init__(self, n_knots):
        self.knots = [(0, 0)] * n_knots

    def update_knot(self, i):
        x_h, y_h = self.knots[i - 1]
        x_t, y_t = self.knots[i]
        dx = x_h - x_t
        dy = y_h - y_t
        if abs(dx) > 1 or abs(dy) > 1:
            x_t += sign(dx)
            y_t += sign(dy)
        self.knots[i] = (x_t, y_t)

    def move(self, direction):
        x, y = self.knots[0]
        match direction:
            case "U":
                y += 1
            case "D":
                y -= 1
            case "R":
                x += 1
            case "L":
                x -= 1
            case _:
                raise ValueError("illegal direction")
        self.knots[0] = (x, y)
        for i in range(1, len(self.knots)):
            self.update_knot(i)

    @property
    def tail(self):
        return self.knots[-1]


def find_n_tail_locs(rope, moves):
    tail_locs = set([rope.tail])
    for mv in moves:
        for _ in range(mv.count):
            rope.move(mv.direction)
            tail_locs.add(rope.tail)
    return len(tail_locs)


def load_moves(path):
    moves = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                direction, count = line.split()
                count = int(count)
                moves.append(Move(direction, count))
    return moves


if __name__ == "__main__":
    import doctest

    doctest.testmod()
