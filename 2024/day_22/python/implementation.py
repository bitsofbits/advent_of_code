from functools import cache
from itertools import pairwise
from collections import defaultdict

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 10, 100, 2024]
    """
    return [int(x) for x in text.strip().split('\n')]

def generate_numbers(x, n):
    """
    >>> x = 123
    >>> for x in generate_numbers(x, 10): print(x)
    15887950
    16495136
    527345
    704524
    1553684
    12683156
    11100544
    12249484
    7753432
    5908254
    """
    for _ in range(n):
        x = (x ^ (x << 6)) % 16777216
        x = (x ^ (x >> 5))# % 16777216
        x = (x ^ (x << 11)) % 16777216
        yield x


@cache
def list_numbers(x, n):
    return list(generate_numbers(x, n))

def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    37327623
    """
    total = 0
    for x in parse(text):
        total += list_numbers(x, 2000)[-1]
    return total

def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    23
    """
    prices_per_pattern = defaultdict(int)
    for x in parse(text):
        # TODO: could use deque to do this incrementally and not build
        # these large arrays
        prices = [x % 10 for x in list_numbers(x, 2000)]
        changes = [b - a for (a, b) in pairwise(prices)]
        seen = set()
        for i in range(2000 - 4):
            pattern = tuple(changes[i:i+4])
            if pattern in seen:
                continue
            seen.add(pattern)
            prices_per_pattern[pattern] += prices[i + 4]
    return max(prices_per_pattern.values())



if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
