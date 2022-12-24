import sys
from time import perf_counter

from implementation import Valley

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    valley = Valley(text)
    path = valley.simple_traverse()
    print(f"Part 1: : {len(path)} ({perf_counter() - t0:.0f}s)")

    valley = Valley(text)
    path = valley.snack_retrieval()
    print(f"Part 2: : {len(path)} ({perf_counter() - t0:.0f}s)")
