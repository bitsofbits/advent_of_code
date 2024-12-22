from functools import cache
from collections import defaultdict


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 10, 100, 2024]
    """
    return [int(x) for x in text.strip().split("\n")]


@cache
def list_numbers(x, n):
    """
    >>> x = 123
    >>> for x in list_numbers(x, 10): print(x)
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
    numbers = []
    for _ in range(n):
        x = (x ^ (x << 6)) % 16777216
        x = (
            x ^ (x >> 5)
        )  # % 16777216, don't need this because we are dividing and already smaller than
        x = (x ^ (x << 11)) % 16777216
        numbers.append(x)
    return numbers


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

    1405
    """
    prices_per_pattern = defaultdict(int)
    key_size = 19
    min_key_value = key_size**3
    for x in parse(text):
        seen = set()
        last_price = x % 10
        key = 0
        for x in list_numbers(x, 2000):
            price = x % 10
            price_change = price - last_price
            last_price = price
            key = (key % min_key_value) * key_size + (price_change + 10)
            if key in seen:
                continue
            seen.add(key)
            prices_per_pattern[key] += price
    return max(v for (k, v) in prices_per_pattern.items() if k >= min_key_value)


print(2147483647, 20**4)

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
