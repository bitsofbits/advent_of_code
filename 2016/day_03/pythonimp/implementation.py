def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))
    [(5, 10, 25), (10, 10, 15), (8, 9, 10)]
    """
    for line in text.strip().split("\n"):
        yield tuple(int(x.strip()) for x in line.split())


def find_triangles(iterable):
    for x in iterable:
        for i in range(3):
            if x[i] >= x[(i + 1) % 3] + x[(i + 2) % 3]:
                break
        else:
            yield x


def ilen(iterable):
    n = 0
    for _ in iterable:
        n += 1
    return n


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    return ilen(find_triangles(parse(text)))


def remap(iterable):
    buf = []
    for x in iterable:
        buf.append(x)
        if len(buf) == 3:
            for i in range(3):
                yield tuple(buf[j][i] for j in range(3))
            buf.clear()


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    return ilen(find_triangles(remap(parse(text))))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
