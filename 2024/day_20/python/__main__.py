import sys
from time import perf_counter

from .implementation import part_1, part_2, part_4

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    value = part_1(text)
    print(f"Part 1: : {value} ({perf_counter() - t0:.2f}s)")

    t0 = perf_counter()
    value = part_2(text)
    print(f"Part 2: : {value} ({perf_counter() - t0:.2f}s)")

    t0 = perf_counter()
    value = part_4(text)
    print(f"Part 4: : {value} ({perf_counter() - t0:.2f}s)")
