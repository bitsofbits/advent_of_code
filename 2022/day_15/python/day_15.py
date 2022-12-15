import sys
from time import perf_counter

from implementation import find_tuning_freq, load_sensors, row_coverage

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    t0 = perf_counter()
    coverage = row_coverage(load_sensors(path), 2000000)
    print(f"Part 1: Row coverage: {coverage} ({perf_counter() - t0})")
    t0 = perf_counter()
    freq = find_tuning_freq(load_sensors(path), 4000000)
    print(f"Part 2: Tuning freq: {freq} ({perf_counter() - t0})")
