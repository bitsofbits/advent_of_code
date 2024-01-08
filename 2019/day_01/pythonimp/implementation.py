from functools import cache


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [12, 14, 1969, 100756]
    """
    return [int(x) for x in text.strip().split()]


def naive_cost(x):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(naive_cost(x))
    2
    2
    654
    33583
    """
    return x // 3 - 2


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    34241
    """
    return sum(naive_cost(x) for x in parse(text))


@cache
def total_cost(x):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(total_cost(x))
    2
    2
    966
    50346
    """
    if x < 9:
        return 0
    immediate_cost = naive_cost(x)
    return immediate_cost + total_cost(immediate_cost)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    51316
    """
    return sum(total_cost(x) for x in parse(text))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
