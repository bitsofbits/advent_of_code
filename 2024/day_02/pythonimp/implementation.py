def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:4]
    [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5]]
    """
    rows = []
    for line in text.strip().split('\n'):
        rows.append([int(x) for x in line.split()])
    return rows


def is_safe(row):
    is_ascending = row[1] > row[0]
    last_x = row[0]
    for x in row[1:]:
        delta = x - last_x
        if not is_ascending:
            delta = -delta
        if delta < 1 or delta > 3:
            return False
        last_x = x
    return True


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    n_safe = 0
    for row in parse(text):
        n_safe += is_safe(row)
    return n_safe


def is_safe_2(row):
    if is_safe(row):
        return True
    for i in range(len(row)):
        sub_row = row[:i] + row[i + 1:]
        if is_safe(sub_row):
            return True
    return False


def part_2(text):
    """
    587 is too low

    >>> part_2(EXAMPLE_TEXT)
    4
    """
    n_safe = 0
    for row in parse(text):
        n_safe += is_safe_2(row)
    return n_safe


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
