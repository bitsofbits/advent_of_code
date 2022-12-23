import sys
from time import perf_counter

from implementation import Board

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    board = Board(text)
    board.move_elves(10)
    print(f"Part 1: : {board.blank_space} ({perf_counter() - t0:.0f}s)")

    board.reset()
    n = board.move_elves(sys.maxsize)
    print(f"Part 2: : {n} ({perf_counter() - t0:.0f}s)")
