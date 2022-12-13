import sys
from time import perf_counter

from implementation import Map, ilen

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    reps = 10
    t0 = perf_counter()
    for _ in range(reps):
        n = ilen(Map(path).find_shortest_path())
    print(f"part-1: {n} ({(perf_counter() - t0) / reps:.3} s)")
    t0 = perf_counter()
    for _ in range(reps):
        n = ilen(Map(path).find_shortest_path(0))
    print(f"part-2: {n} ({(perf_counter() - t0) / reps:.3} s)")
