import sys

from implementation import compute_business, load_monkeys

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    print(compute_business(load_monkeys(path, 3), 20))
    print(compute_business(load_monkeys(path, 1), 10000))
