def parse_block(text):
    block = set()
    max_i = max_j = 0
    for i, line in enumerate(text.strip().split('\n')):
        line = line.strip()
        max_i = max(i, max_i)
        for j, x in enumerate(line):
            max_j = max(j, max_j)
            if x == '#':
                block.add((i, j))
    return block, max_i, max_j


def parse(text):
    for block in text.strip().split('\n\n'):
        yield parse_block(block)


def find_horizontal_reflections(block, max_i, max_j):
    by_col = [set() for _ in range(max_j + 1)]
    for i, j in block:
        by_col[j].add(i)
    by_col = tuple(frozenset(x) for x in by_col)
    for j in range(1, max_j + 1):
        right_cols = by_col[j : 2 * j][::-1]
        left_cols = by_col[j - len(right_cols) : j]
        if left_cols == right_cols:
            yield j


def find_vertical_reflections(block, max_i, max_j):
    transposed = set((j, i) for (i, j) in block)
    return find_horizontal_reflections(transposed, max_j, max_i)


def score(block, max_i, max_j):
    h = find_horizontal_reflections(block, max_i, max_j)
    v = find_vertical_reflections(block, max_i, max_j)
    return sum(h, 0) + 100 * sum(v, 0)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    405
    """
    total = 0
    for i, (block, max_i, max_j) in enumerate(parse(text)):
        total += score(block, max_i, max_j)
    return total


def desmudged_score(block, max_i, max_j):
    h0 = set(find_horizontal_reflections(block, max_i, max_j))
    v0 = set(find_vertical_reflections(block, max_i, max_j))
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            block ^= {(i, j)}
            try:
                h = set(find_horizontal_reflections(block, max_i, max_j)) - h0
                if h:
                    [h] = h
                    return h
                v = set(find_vertical_reflections(block, max_i, max_j)) - v0
                if v:
                    [v] = v
                    return 100 * v
            finally:
                block ^= {(i, j)}


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    400
    """
    total = 0
    for i, (block, max_i, max_j) in enumerate(parse(text)):
        x = desmudged_score(block, max_i, max_j)
        if x is None:
            print(i, "can't be desmudged")
        else:
            total += x
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
