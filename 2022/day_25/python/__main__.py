import sys
from time import perf_counter

from implementation import part_1

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    value = part_1(text)
    print(f"Part 1: : {value} ({perf_counter() - t0:.1f}s)")

    # valley = Valley(text)
    # path = valley.snack_retrieval()
    # print(f"Part 2: : {len(path)} ({perf_counter() - t0:.1f}s)")
