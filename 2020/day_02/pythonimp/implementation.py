# 7-11 m: mmmmmmsmmmmm


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('a', 1, 3, 'abcde')
    ('b', 1, 3, 'cdefg')
    ('c', 2, 9, 'ccccccccc')
    """
    for line in text.strip().split("\n"):
        rule, string = line.split(": ")
        rng, char = rule.split()
        a, b = (int(x) for x in rng.split("-"))
        yield char, a, b, string


def count(char, string):
    cnt = 0
    for c in string:
        if c == char:
            cnt += 1
    return cnt


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    n_valid = 0
    for char, a, b, string in parse(text):
        if a <= count(char, string) <= b:
            n_valid += 1
    return n_valid


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1
    """  # 413 is too high
    n_valid = 0
    for char, a, b, string in parse(text):
        if (string[a - 1] == char) ^ (string[b - 1] == char):
            n_valid += 1
    return n_valid


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
