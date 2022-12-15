import sys

from implementation import find_tuning_freq, load_sensors, row_coverage

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    coverage = row_coverage(load_sensors(path), 2000000)
    print("Part 1: Row coverage:", coverage)
    freq = find_tuning_freq(load_sensors(path), 4000000)
    print("Part 2: Tuning freq", freq)
