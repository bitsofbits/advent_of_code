import sys
from collections import deque


def load_input(path):
    with open(path) as f:
        return f.read()


def find_unique_run_location(txt, run_length):
    n = run_length - 1
    prefix = deque(maxlen=n)
    for i, x in enumerate(txt):
        if len(set(prefix)) == n and x not in prefix:
            return i + 1
        prefix.append(x)
    raise ValueError("No dup free regions")


if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    text = load_input(path)
    print(find_unique_run_location(text, 4))
    print(find_unique_run_location(text, 14))
