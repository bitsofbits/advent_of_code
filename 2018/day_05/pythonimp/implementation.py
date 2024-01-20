from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    deque(['d', 'a', 'b', 'A', 'c', 'C', 'a', 'C', 'B', 'A', 'c', 'C', 'c', 'a', 'D', 'A'])
    """
    return deque(text.strip())


def lower(x):
    if x is None:
        return None
    return x.lower()


def react_left(p):
    # Could use +- numbers instead
    while lower(p[0]) == lower(p[1]) and p[0] != p[1]:
        p.popleft()
        p.popleft()


def react(p):
    last_length = 2 * len(p)
    while len(p) != last_length:
        for _ in range(len(p)):
            react_left(p)
            p.rotate(1)
        last_length = len(p)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    10
    """
    p = parse(text)
    # It's convenient to use circular linked list (queue) but can't react across
    # zero so put a non reactive element in and remove later
    p.appendleft(None)
    react(p)
    return len(p) - 1


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    4
    """
    p = parse(text)
    # It's convenient to use circular linked list (queue) but can't react across
    # zero so put a non reactive element in and remove later
    p.appendleft(None)
    min_length = len(p)
    for i in range(26):
        dropped = {chr(ord('a') + i), chr(ord('A') + i)}
        candidate = deque([x for x in p if x not in dropped])
        react(candidate)
        if len(candidate) < min_length:
            min_length = len(candidate)
    return min_length - 1


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
