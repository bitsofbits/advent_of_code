def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    """
    return [int(x) for x in text.strip().split()]


# A header, which is always exactly two numbers:
# The quantity of child nodes.
# The quantity of metadata entries.
# Zero or more child nodes (as specified in the header).
# One or more metadata entries (as specified in the header).


def sum_metadata(stream, i0=0):
    total = 0
    n_child = stream[i0]
    n_meta = stream[i0 + 1]
    i0 += 2
    for _ in range(n_child):
        subtotal, i0 = sum_metadata(stream, i0)
        total += subtotal
    total += sum(stream[i0 : i0 + n_meta])
    return total, i0 + n_meta


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    138
    """
    return sum_metadata(parse(text))[0]


def node_a_value(stream, i0=0):
    n_child = stream[i0]
    n_meta = stream[i0 + 1]
    i0 += 2
    if n_child == 0:
        return sum(stream[i0 : i0 + n_meta]), i0 + n_meta
    else:
        child_values = []
        for _ in range(n_child):
            subtotal, i0 = node_a_value(stream, i0)
            child_values.append(subtotal)
        total = 0
        for i in range(n_meta):
            n = stream[i0 + i] - 1
            assert n >= 0
            if n < len(child_values):
                total += child_values[n]
        return total, i0 + n_meta


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    66
    """
    return node_a_value(parse(text))[0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
