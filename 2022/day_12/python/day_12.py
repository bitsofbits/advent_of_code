import sys
from time import perf_counter

from implementation import Map

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    t0 = perf_counter()
    n = len(Map(path).find_shortest_path())
    print(f"part-1 took {perf_counter() - t0} s")
    print(n)
    t0 = perf_counter()
    n = len(Map(path).find_shortest_path({"a", "S"}))
    print(f"part-2 took {perf_counter() - t0} s")
    print(n)
