from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    3
    """
    return int(text.strip())


def fill_spinlock(n, cnt):
    buffer = deque([0])
    for i in range(1, cnt):
        shift = (n + 1) % len(buffer)
        buffer.rotate(-shift)
        buffer.appendleft(i)
    return buffer


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    638
    """
    buffer = fill_spinlock(parse(text), 2018)
    buffer.rotate(-1)
    return buffer.popleft()


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1222153
    """
    buffer = fill_spinlock(parse(text), 50_000_000)
    first = None
    while buffer:
        x = buffer.popleft()
        if x == 0:
            break
        if first is None:
            first = x
    else:
        return first
    return buffer.popleft()


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
