def render(disk_map):
    return ''.join('.' if (x is None) else chr(x + ord('0')) for x in disk_map)


def parse(text):
    """
    >>> render(parse(EXAMPLE_TEXT)[-1])
    '00...111...2...333.44.5555.6666.777.888899'
    """
    text = text.strip()
    n = len(text)
    assert n % 2 == 1, n
    text += '0'
    sparse_map = []
    location = 0
    for i in range(0, n, 2):
        block_size, gap_size = (int(x) for x in text[i:i + 2])
        sparse_map.append((location, block_size))
        location += block_size + gap_size

    size = max(loc + delta for (loc, delta) in sparse_map)
    dense_map = [None] * size
    for id_, (location, block_size) in enumerate(sparse_map):
        for i in range(location, location + block_size):
            dense_map[i] = id_

    return sparse_map, dense_map


def checksum(disk_map):
    return sum( (i *x) for  (i, x) in enumerate(disk_map) if x is not None)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1928
    """
    *_, dense_map = parse(text)

    empty = [i for (i, x) in enumerate(dense_map) if x is None]
    empty.reverse()
    for i in reversed(range(len(dense_map))):
        if dense_map[i] is None:
            continue
        if not empty:
            break
        j = empty.pop()
        if i < j:
            continue
        dense_map[j] = dense_map[i]
        dense_map[i] = None
    return checksum(dense_map)


def build_gap_map(dense_map):
    gap_map = []
    start = None
    for i, x in enumerate(dense_map):
        if start is None:
            if x is None:
                start = i
        else:
            if x is not None:
                gap_map.append((start, i - start))
                start = None
    if start is not None:
        gap_map.append((start, len(dense_map) - start))
    return gap_map


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2858
    """
    sparse_map, dense_map = parse(text)

    for i in reversed(range(len(sparse_map))):
        block_loc, block_size = sparse_map[i]
        gap_map = build_gap_map(dense_map)
        for j, (gap_loc, gap_size) in enumerate(gap_map):
            if gap_loc > block_loc:
                break
            if gap_size < block_size:
                continue
            for k in range(block_size):
                dense_map[gap_loc + k] = dense_map[block_loc + k]
                dense_map[block_loc + k] = None
                gap_map[j] = (gap_loc + block_size, gap_size - block_size)
    return checksum(dense_map)

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
