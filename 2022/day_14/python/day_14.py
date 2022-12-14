import sys

from implementation import Cave

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    with open(path) as f:
        text = f.read()

    n_units = Cave(text).fill_with_sand()
    print("Part 1: Number of units of sand:", n_units)
    n_units = Cave(text, has_floor=True).fill_with_sand()
    print("Part 1: Number of units of sand:", n_units)
