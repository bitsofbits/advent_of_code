def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    (0, 2)
    (2, 2)
    (2, 3)
    (3, 4)
    (3, 5)
    (0, 1)
    (10, 1)
    (9, 10)
    """
    for line in text.strip().split("\n"):
        a, b = line.strip().split("/")
        yield int(a), int(b)


def assemble(parts):
    n = len(parts)
    stack = []
    for i, (a, b) in enumerate(parts):
        a, b = parts[i]
        if a == 0 or b == 0:
            available = frozenset(j for j in range(n) if j != i)
            if a == 0:
                stack.append((b, available, b))
            if b == 0:
                stack.append((a, available, a))

    best_strength = max(s for (_, _, s) in stack)
    while stack:
        b, available, s = stack.pop()
        best_strength = max(s, best_strength)
        for next_i in available:
            p0, p1 = parts[next_i]
            next_available = None
            for next_a, next_b in [(p0, p1), (p1, p0)]:
                if next_a != b:
                    continue
                if next_available is None:
                    next_available = available - {next_i}
                next_s = s + next_a + next_b
                stack.append((next_b, next_available, next_s))
    return best_strength


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    31
    """
    parts = list(parse(text))
    return assemble(parts)


def assemble_long(parts):
    n = len(parts)
    stack = []
    for i, (a, b) in enumerate(parts):
        a, b = parts[i]
        if a == 0 or b == 0:
            available = frozenset(j for j in range(n) if j != i)
            if a == 0:
                stack.append((b, available, b))
            if b == 0:
                stack.append((a, available, a))

    best = (1, max(s for (_, _, s) in stack))
    while stack:
        b, available, s = stack.pop()
        if (n - len(available), s) > best:
            best = (n - len(available), s)
        for next_i in available:
            p0, p1 = parts[next_i]
            next_available = None
            for next_a, next_b in [(p0, p1), (p1, p0)]:
                if next_a != b:
                    continue
                if next_available is None:
                    next_available = available - {next_i}
                next_s = s + next_a + next_b
                stack.append((next_b, next_available, next_s))
    _, s = best
    return s


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    19
    """
    parts = list(parse(text))
    return assemble_long(parts)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
