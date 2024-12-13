import re
from functools import cache

pattern_text = r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)"""


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[0]
    ((94, 34), (22, 67), (8400, 5400))
    """
    pattern = re.compile(pattern_text)
    machines = []
    for chunk in text.strip().split("\n\n"):
        vals = [int(x) for x in pattern.match(chunk).groups()]
        machines.append((tuple(vals[:2]), tuple(vals[2:4]), tuple(vals[4:])))
    return machines


@cache
def compute_deltas(machine, da=1, db=1, max_ndx=100):
    (di_a, dj_a), (di_b, dj_b), (i, j) = machine
    deltas = {}
    for a in range(1, max_ndx + 1, da):
        a_di_a = a * di_a
        a_dj_a = a * dj_a
        for b in range(1, max_ndx + 1, db):
            delta_i = i - (a_di_a + b * di_b)
            delta_j = j - (a_dj_a + b * dj_b)
            key = (delta_i, delta_j)
            cost = 3 * a + b
            if delta_i == delta_j:
                if key not in deltas:
                    deltas[key] = cost
                else:
                    deltas[key] = min(cost, deltas[key])
    return deltas


def part_1_orig(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    480
    """
    machines = parse(text)
    cost = 0
    for machine in machines:
        deltas = compute_deltas(machine)
        cost += deltas.get((0, 0), 0)
    return cost

def det(x):
    # Only valid for 2x2 case
    return x[0][0] * x[1][1] - x[0][1] * x[1][0] 

def solve(A, v):
    # Only valid for 2x2 case
    d = det(A)
    [[a11, a12], [a21, a22]] = A
    [v1, v2] = v
    # Solve using Cramer's rule
    x1 = det([[v1, a12], [v2, a22]]) / d
    x2 = det([[a11, v1], [a21, v2]]) / d
    return x1, x2

def mult(A, x):
    # only valid for 2x2 matrices
    [[a11, a12], [a21, a22]] = A
    [x1, x2] = x
    return [a11 * x1 + a12 * x2, a21 * x1 + a22 * x2]

def solve_machine(machine):
    (di_a, dj_a), (di_b, dj_b), (i, j) = machine

    A = [[di_a, di_b], [dj_a, dj_b]]
    v = [i, j]

    a, b = (int(round(x)) for x in solve(A, v))
    if det(A) == 0:
        # Could be handled but turns out we don't need to
        raise ValueError("degenerate")

    import numpy as np
    if mult(A, [a, b]) == v:
        return 3 * a + b
    return None


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    480
    """
    machines = parse(text)
    cost = 0
    for machine in machines:
        machine_cost = solve_machine(machine)
        if machine_cost is not None:
            cost += machine_cost
    return cost


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    875318608908
    """
    offset = 10000000000000
    machines = parse(text)
    cost = 0
    for machine in machines:
        (di_a, dj_a), (di_b, dj_b), (i, j) = machine
        machine = (di_a, dj_a), (di_b, dj_b), (i + offset, j + offset)
        machine_cost = solve_machine(machine)
        if machine_cost is not None:
            cost += machine_cost
    return cost


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
