from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    5
    """
    return int(text.strip())


def play(n):
    circle = deque(i + 1 for i in range(n))
    while len(circle) > 1:
        circle.rotate(-1)
        circle.popleft()
    return circle.pop()


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    n = parse(text)
    return play(n)


def play2_slow(n):
    """
    >>> play2_slow(6)
    3
    >>> play2_slow(7)
    5
    """
    circle = deque(i + 1 for i in range(n))
    while n > 1:
        d = n // 2
        circle.rotate(-d)
        circle.popleft()
        circle.rotate(d - 1)
        n = len(circle)
    return circle.pop()


def play2(n):
    """
    >>> play2(5)  # 3, 5, 1, 4
    2
    >>> play2(6)
    3
    >>> play2(7)
    5
    """
    circle = deque(i + 1 for i in range(n))
    circle.rotate(-(n // 2))
    while n > 1:
        circle.popleft()
        circle.rotate(-(n % 2))
        n = len(circle)
    return circle.pop()


# 1739658 is too high


def part_2(text):
    """
    # >>> part_2(EXAMPLE_TEXT)
    # 2
    """
    n = parse(text)
    return play2(n)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
