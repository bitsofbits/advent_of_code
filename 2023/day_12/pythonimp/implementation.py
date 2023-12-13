from functools import cache


def parse(text):
    """
    >>> _ = parse(EXAMPLE_TEXT)
    """
    records = []
    for line in text.strip().split('\n'):
        record, count_text = line.split()
        counts = tuple(int(x) for x in count_text.split(','))
        records.append((record, counts))
    return records


@cache
def _count_valid(seq, counts):
    seq = seq.lstrip('.')
    if not seq:
        return not counts
    if not counts:
        return 0 if ('#' in seq) else 1
    required = counts[0]
    first_known_dot = seq.index('.')
    if first_known_dot < required:
        has_spring = '#' in seq[:first_known_dot]
        return 0 if has_spring else _count_valid(seq[first_known_dot + 1 :], counts)
    available = first_known_dot - required + 1
    count = 0
    for i in range(available):
        break_available = seq[i + required] in '.?'
        if break_available:
            count += _count_valid(seq[i + required + 1 :], counts[1:])
        at_a_spring = seq[i] == '#'
        if at_a_spring:
            # Can't proceed since current count _must_ start here
            return count
    counts_if_skip_this_block = _count_valid(seq[available:], counts)
    return count + counts_if_skip_this_block


def count_valid(seq, counts):
    # Ensure all sequences end with '.' so can remove check in _count_valid
    seq = seq + '.'
    return _count_valid(seq, counts)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    21
    """
    records = parse(text)
    total = 0
    for record, counts in records:
        valid = count_valid(record, counts)
        total += valid
    return total


def unfold(record, counts, n=5):
    """
    >>> unfold('.#', (1,))
    ('.#?.#?.#?.#?.#', (1, 1, 1, 1, 1))
    """
    return '?'.join([record] * n), counts * n


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    525152

    # 1493340882140
    """
    records = parse(text)
    total = 0
    for record, counts in records:
        record, counts = unfold(record, counts)
        valid = count_valid(record, counts)
        total += valid
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
