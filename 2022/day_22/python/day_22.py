import sys
from time import perf_counter

from implementation import parse_text

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    board, moves = parse_text(text)
    board.move(moves)
    print(f"Part 1: : {board.password} ({perf_counter() - t0:.0f}s)")

    board, moves = parse_text(text)
    board.move(moves, cube_wrap=True)
    print(f"Part 2: : {board.password} ({perf_counter() - t0:.0f}s)")
