import sys
from time import perf_counter

from implementation import (add_paths, dual_traverse, parse_graph, simplify,
                            traverse)

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    t0 = perf_counter()
    with open(path) as f:
        text = f.read()
    nodes = simplify(parse_graph(text))
    add_paths(nodes)
    print(f"Setting up graph took ({perf_counter() - t0:.2}s)")

    t0 = perf_counter()
    pressure = traverse(nodes, 30)
    print(f"Part 1: Max pressure release: {pressure} ({perf_counter() - t0:.2}s)")
    t0 = perf_counter()
    freq = dual_traverse(nodes, 26)
    print(f"Part 2: Dual max pressure release: {freq} ({perf_counter() - t0:.2}s)")
