import numpy as np

INITIAL_PATTERN = """
.#.
..#
###
""".strip()


def text_to_array(text):
    l = []
    for line in text:
        row = []
        for c in line:
            row.append(0 if (c == ".") else 1)
        l.append(row)
    return np.array(l)


def parse_pattern(p):
    p = p.strip()
    return text_to_array([x for x in p.split("/")])


def parse_line(line):
    src, tgt = line.split("=>")
    return parse_pattern(src), parse_pattern(tgt)


def a2t(a):
    l = []
    for row in a:
        r = []
        for x in row:
            r.append("." if (x == 0) else "#")
        l.append("".join(r))
    return tuple(l)


def parse(text):
    """
    >>> for src, tgt in parse(EXAMPLE_TEXT): print(a2t(src), a2t(tgt))
    ('..', '.#') ('##.', '#..', '...')
    ('.#.', '..#', '###') ('#..#', '....', '....', '#..#')
    """
    for line in text.strip().split("\n"):
        yield parse_line(line)


def key(x):
    return tuple(tuple(row) for row in x)


def build_mapping(base):
    # Maps arrays to arrays, but arrays aren't hashable so
    # create a tuple version as lookup
    mapping = {}
    for src, tgt in base:
        mapping[key(src)] = tgt
        mapping[key(src[::-1, :])] = tgt
        mapping[key(src[:, ::-1])] = tgt
        mapping[key(src[::-1, ::-1])] = tgt
        src = src.transpose()
        mapping[key(src)] = tgt
        mapping[key(src[::-1, :])] = tgt
        mapping[key(src[:, ::-1])] = tgt
        mapping[key(src[::-1, ::-1])] = tgt
    return mapping


def part_1(text, iterations=5):
    """
    >>> part_1(EXAMPLE_TEXT, iterations=2)
    12
    """
    base = parse(text)
    mapping = build_mapping(base)
    pattern = text_to_array(INITIAL_PATTERN.split("\n"))
    assert pattern.shape[0] == pattern.shape[1]
    for _ in range(iterations):
        size = len(pattern)
        if size % 2 == 0:
            pattern = pattern.reshape(size // 2, 2, size // 2, 2)
            pattern = pattern.transpose(0, 2, 1, 3)
            pattern = pattern.reshape(-1, 2, 2)
            dx = 3
        else:
            assert size % 3 == 0
            pattern = pattern.reshape(size // 3, 3, size // 3, 3)
            pattern = pattern.transpose(0, 2, 1, 3)
            pattern = pattern.reshape(-1, 3, 3)
            dx = 4
        new_pattern = [mapping[key(x)] for x in pattern]
        new_pattern = np.array(new_pattern)
        dy = int(np.sqrt(new_pattern.size // dx**2))
        pattern = new_pattern.reshape(dy, dy, dx, dx)
        pattern = pattern.transpose(0, 2, 1, 3)
        pattern = pattern.reshape(dx * dy, dx * dy)

    return pattern.sum()


def part_2(text):
    return part_1(text, iterations=18)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
