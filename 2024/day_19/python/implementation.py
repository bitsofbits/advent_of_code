from functools import cache

def parse(text):
    """
    >>> towels, patterns = parse(EXAMPLE_TEXT)
    >>> towels
    ('r', 'wr', 'b', 'g', 'bwu', 'rb', 'gb', 'br')
    >>> patterns
    ['brwrr', 'bggr', 'gbbr', 'rrbgbr', 'ubwu', 'bwurrg', 'brgr', 'bbrgwb']
    """
    towels, patterns = text.strip().split('\n\n')
    towels = [x.strip() for x in towels.split(',')]
    patterns = [x.strip() for x in patterns.split()]
    return tuple(towels), patterns

@cache
def can_make(pattern, towels):
    for x in towels:
        if x == pattern:
            return True
        if pattern.startswith(x):
            if can_make(pattern[len(x):], towels):
                return True
    return False


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    6
    """
    towels, patterns = parse(text)
    return sum(can_make(x, towels) for x in patterns)



@cache
def can_make_count(pattern, towels):
    if not pattern:
        return 0
    count = 0
    for x in towels:
        if x == pattern:
            count += 1
        elif pattern.startswith(x):
            count += can_make_count(pattern[len(x):], towels)
    return count



def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    16
    """
    towels, patterns = parse(text)
    return sum(can_make_count(x, towels) for x in patterns)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
