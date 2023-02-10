def parse_line(line, which):
    _, w, _, _, n = line.strip().split()
    assert w == which
    return int(n)


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))
    [65, 8921]
    """
    for line, which in zip(text.strip().split("\n"), "AB"):
        yield parse_line(line, which)


def generator(start, mult):
    x = start
    while True:
        x = (x * mult) % 2_147_483_647
        yield x


def part_1(text, count=40_000_000):
    """
    >>> part_1(EXAMPLE_TEXT, count=5) # 588
    1
    >>> part_1(EXAMPLE_TEXT)
    588
    """
    a0, b0 = parse(text)
    A = generator(a0, 16807)
    B = generator(b0, 48271)
    matching = 0
    for i, (a, b) in enumerate(zip(A, B)):
        if i >= count:
            break
        if (a & 0xFFFF) == (b & 0xFFFF):
            matching += 1
    return matching


def picky_generator(start, mult, divisor):
    x = start
    while True:
        x = (x * mult) % 2_147_483_647
        if x % divisor == 0:
            yield x


def part_2(text, count=5_000_000):
    """
    >>> part_2(EXAMPLE_TEXT)
    309
    """
    a0, b0 = parse(text)
    A = picky_generator(a0, 16807, 4)
    B = picky_generator(b0, 48271, 8)
    matching = 0
    for i, (a, b) in enumerate(zip(A, B)):
        if i >= count:
            break
        if (a & 0xFFFF) == (b & 0xFFFF):
            matching += 1
    return matching


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
