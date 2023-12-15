from functools import cache
from multiprocessing import Pool


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
    if not counts:
        return 0 if ('#' in seq) else 1
    if len(seq) - seq.count('.') < sum(counts):
        return 0
    first_known_dot = seq.index('.')
    required = counts[0]
    if first_known_dot < required:
        if '#' in seq[:first_known_dot]:
            return 0
        else:
            return _count_valid(seq[first_known_dot + 1 :], counts)
    available = first_known_dot - required + 1
    count = 0
    for i in range(available):
        break_available = seq[i + required] != '#'
        if break_available:
            count += _count_valid(seq[i + required + 1 :], counts[1:])
        if seq[i] == '#':
            # Can't proceed since current count _must_ start here
            return count
    return count + _count_valid(seq[available:], counts)


def count_valid(record):
    seq, counts = record
    # Ensure all sequences end with '.' so can remove check in _count_valid
    seq = seq.lstrip('.') + '.'
    return _count_valid(seq, counts)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    21
    """
    records = parse(text)
    return sum(map(count_valid, records))


def unfold(record, counts, n=5):
    """
    >>> unfold('.#', (1,))
    ('.#?.#?.#?.#?.#', (1, 1, 1, 1, 1))
    """
    return '?'.join([record] * n), counts * n


def part_2(text, use_multiprocessing=True):
    """
    >>> part_2(EXAMPLE_TEXT)
    525152

    # 1493340882140
    """
    records = parse(text)
    records = [unfold(record, counts) for record, counts in records]
    if use_multiprocessing:
        with Pool(8) as p:
            return sum(p.imap_unordered(count_valid, records, chunksize=10))
    else:
        return sum(map(count_valid, records))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
