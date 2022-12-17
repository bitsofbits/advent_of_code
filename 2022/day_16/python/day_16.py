import sys
from time import perf_counter

from implementation import (dual_max_pressure_release, max_pressure_release,
                            parse_graph)

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    nodes = parse_graph(text)
    # pressure = max_pressure_release(nodes)
    # print(f"Part 1: Max pressure release: {pressure} ({perf_counter() - t0})")
    t0 = perf_counter()
    freq = dual_max_pressure_release(nodes)
    print(f"Part 2: Dual max pressure release: {freq} ({perf_counter() - t0})")
