def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ['ULL', 'RRDDD', 'LURDL', 'UUUUD']
    """
    return [x.strip() for x in text.strip().split("\n")]


KEYPAD1 = {(i, j): str(3 * i + j + 1) for i in range(3) for j in range(3)}


KEYPAD2 = {
    (0, 2): "1",
    (1, 1): "2",
    (1, 2): "3",
    (1, 3): "4",
    (2, 0): "5",
    (2, 1): "6",
    (2, 2): "7",
    (2, 3): "8",
    (2, 4): "9",
    (3, 1): "A",
    (3, 2): "B",
    (3, 3): "C",
    (4, 2): "D",
}


def decode(code, i, j, keypad):
    """
    >>> decode("ULL", 2, 0, KEYPAD2)
    (2, 0)
    >>> decode("ULL", 2, 0, KEYPAD2)
    (2, 0)
    """
    for x in code:
        i0, j0 = i, j
        match x:
            case "U":
                i -= 1
            case "D":
                i += 1
            case "L":
                j -= 1
            case "R":
                j += 1
            case _:
                raise ValueError(x)
        if (i, j) not in keypad:
            i, j = i0, j0
    return i, j


def find_code(codes, keypad):
    """
    >>> codes = parse(EXAMPLE_TEXT)
    >>> list(find_code(codes, KEYPAD2))
    ['5', 'D', 'B', '3']
    """
    for k, v in keypad.items():
        if v == "5":
            break
    else:
        raise RuntimeError()
    i, j = k
    for c in codes:
        i, j = decode(c, i, j, keypad)
        yield keypad[i, j]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    '1985'
    """
    return "".join(find_code(parse(text), KEYPAD1))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    '5DB3'
    """
    return "".join(find_code(parse(text), KEYPAD2))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
