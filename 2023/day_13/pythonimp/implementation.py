from functools import lru_cache


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
    n_rows = max_i + 1
    n_cols = max_j + 1
    return frozenset(block), n_rows, n_cols


def parse(text):
    for block in text.strip().split('\n\n'):
        yield parse_block(block)


@lru_cache
def compute_by_col(block, n_cols):
    by_col = [0 for _ in range(n_cols)]
    for i, j in block:
        by_col[j] |= 1 << i
    return by_col


def find_horizontal_reflections(block, n_rows, n_cols, toggle=None):
    by_col = compute_by_col(block, n_cols)
    if toggle is not None:
        by_col = list(by_col)
        i, j = toggle
        by_col[j] ^= 1 << i
    for j in range(1, n_cols):
        right_cols = by_col[2 * j - 1 : j - 1 : -1]
        left_cols = by_col[j - len(right_cols) : j]
        if left_cols == right_cols:
            yield j


def find_vertical_reflections(block, n_rows, n_cols, toggle=None):
    block = frozenset((j, i) for (i, j) in block)
    toggle = toggle if (toggle is None) else toggle[::-1]
    return find_horizontal_reflections(block, n_cols, n_rows, toggle=toggle)


def score(block, n_rows, n_cols):
    h = find_horizontal_reflections(block, n_rows, n_cols)
    v = find_vertical_reflections(block, n_rows, n_cols)
    return sum(h, 0) + 100 * sum(v, 0)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    405

    34918
    """
    total = 0
    for i, (block, n_rows, n_cols) in enumerate(parse(text)):
        total += score(block, n_rows, n_cols)
    return total


def _unpack(iterable):
    # If there is anything here, return the first (and only item)
    for x in iterable:
        return x
        break
    else:
        # Otherwise return None
        return None
    raise ValueError("should only be 0 or 1 items")


def desmudged_score(block, n_rows, n_cols):
    h0 = _unpack(find_horizontal_reflections(block, n_rows, n_cols))
    v0 = _unpack(find_vertical_reflections(block, n_rows, n_cols))
    for i in range(n_rows):
        for j in range(n_cols):
            for h in find_horizontal_reflections(block, n_rows, n_cols, toggle=(i, j)):
                if h != h0:
                    return h
            for v in find_vertical_reflections(block, n_rows, n_cols, toggle=(i, j)):
                if v != v0:
                    return 100 * v


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    400

    # 33054
    """
    total = 0
    for i, (block, max_i, max_j) in enumerate(parse(text)):
        x = desmudged_score(block, max_i, max_j)
        total += x
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
