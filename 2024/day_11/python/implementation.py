from functools import cache
from collections import defaultdict

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [125, 17]
    """
    return [int(x) for x in text.strip().split()]

@cache
def morph(x):
    """
    >>> morph(0)
    [1]
    >>> morph(3)
    [6072]
    >>> morph(22)
    [2, 2]
    >>> morph(1000)
    [10, 0]
    >>> morph(1001)
    [10, 1]
    """
    if x == 0:
        return (1,)
    digits = 0
    y = x
    while y:
        y //= 10
        digits += 1
    if digits % 2 == 0:
        return divmod(x, 10 ** (digits // 2))
    return (x * 2024,)

def part_1(text, iterations=25):
    """
    >>> part_1(EXAMPLE_TEXT)
    55312
    """
    stones = parse(text)
    counts = defaultdict(int)
    for k in stones:
        counts[k] += 1
    for _ in range(iterations):
        next_counts = defaultdict(int)
        for k0, n in counts.items():
            for k1 in morph(k0):
                next_counts[k1] += n
        counts = next_counts
    return sum(counts.values())

def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    65601038650482
    """
    return part_1(text, iterations=75)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
