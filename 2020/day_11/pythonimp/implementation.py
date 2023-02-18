from collections import defaultdict
from itertools import count

import numpy as np


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT).astype(int)
    array([[1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
           [1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
           [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
           [1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
           [1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
           [0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
           [1, 0, 1, 1, 1, 1, 1, 0, 1, 1]])
    """
    rows = []
    for line in text.strip().split("\n"):
        rows.append([(x == "L") for x in line])
    return np.array(rows)


def step(full, seats):
    H, W = full.shape
    padded_adjacent_count = np.zeros((H + 2, W + 2), dtype=int)
    for di in [0, 1, 2]:
        for dj in [0, 1, 2]:
            padded_adjacent_count[di : H + di, dj : W + dj] += full
    adjacent_count = padded_adjacent_count[1:-1, 1:-1]
    empty = (~full) & seats
    return (empty & (adjacent_count == 0)) | (full & (adjacent_count <= 4))


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    37
    """
    seats = parse(text)
    a = np.zeros_like(seats)
    while True:
        next_a = step(a, seats)
        if np.alltrue(next_a == a):
            break
        a = next_a
    return a.sum()


def find_neighbors(seats):
    H, W = seats.shape
    nbrs = {}
    for i0 in range(H):
        for j0 in range(W):
            if not seats[i0, j0]:
                continue
            nbrs[i0, j0] = [(i0, j0)]
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == dj == 0:
                        continue
                    for n in count(1):
                        i, j = i0 + di * n, j0 + dj * n
                        if not (0 <= i < H and 0 <= j < W):
                            break
                        if seats[i, j]:
                            nbrs[i0, j0].append((i, j))
                            break
    return dict(nbrs)


def step2(full, seats, nbrs):
    H, W = full.shape
    adjacent_count = np.zeros((H, W), dtype=int)
    for k0, nbrs in nbrs.items():
        adjacent_count[k0] = sum(full[k1] for k1 in nbrs)
    empty = (~full) & seats
    return (empty & (adjacent_count == 0)) | (full & (adjacent_count <= 5))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    26
    """
    seats = parse(text)
    nbrs = find_neighbors(seats)
    a = np.zeros_like(seats)
    while True:
        next_a = step2(a, seats, nbrs)
        if np.alltrue(next_a == a):
            break
        a = next_a
    return a.sum()


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
