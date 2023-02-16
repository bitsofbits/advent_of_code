from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:10]
    [35, 20, 15, 25, 47, 40, 62, 55, 65, 95]
    """
    return [int(x) for x in text.strip().split()]


def check(n, q):
    for i, x in enumerate(q):
        for j, y in enumerate(q):
            if j >= i:
                break
            if x + y == n:
                return True
    return False


def find_invalid(numbers, preamble):
    q = deque(maxlen=preamble)
    for x in numbers:
        if len(q) >= preamble:
            if not check(x, q):
                return x
        q.append(x)
    raise ValueError("find_invalid did not terminate")


def part_1(text, preamble=25):
    """
    >>> part_1(EXAMPLE_TEXT, 5)
    127
    """
    numbers = parse(text)
    return find_invalid(numbers, preamble)


def part_2(text, preamble=25):
    """
    >>> part_2(EXAMPLE_TEXT, 5)
    62
    """
    numbers = parse(text)
    invalid = find_invalid(numbers, preamble)
    N = len(numbers)
    for i, x in enumerate(numbers[:-1]):
        total = x
        for j in range(i + 1, N):
            y = numbers[j]
            total += y
            if total == invalid:
                run = sorted(numbers[i : j + 1])
                return run[0] + run[-1]
    # raise ValueError("did not terminate")


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
