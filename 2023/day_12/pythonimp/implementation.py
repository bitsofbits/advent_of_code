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


def find_groups(seq):
    """
    >>> find_groups('.#.###.#.######')
    (1, 3, 1, 6)
    >>> find_groups('####.#...#...')
    (4, 1, 1)
    """
    assert set(seq).issubset({'#', '.'}), seq
    groups = []
    start = None
    for i, x in enumerate(seq):
        if start is None:
            if x == '#':
                start = i
        else:
            if x == '.':
                groups.append(i - start)
                start = None
    if start is not None:
        groups.append(i - start + 1)
    return tuple(groups)


def permute_record(seq):
    """
    >>> list(permute_record('????.#...#...'))[:3]
    ['.....#...#...', '#....#...#...', '.#...#...#...']
    """
    indices = [i for (i, x) in enumerate(seq) if x == '?']
    n_bits = len(indices)
    for i in range(2**n_bits):
        permuted = list(seq)
        for j, index in enumerate(indices):
            x = '#' if (i // 2**j) % 2 else '.'
            permuted[index] = x
        yield ''.join(permuted)


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


def unfold(record, counts):
    """
    >>> unfold('.#', (1,))
    ('.#?.#?.#?.#?.#', (1, 1, 1, 1, 1))
    """
    n = 5
    return '?'.join([record] * n), counts * n


# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 4 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 1 arrangement
# ????.######..#####. 1,6,5 - 4 arrangements
# ?###???????? 3,2,1 - 10 arrangements


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    525152
    """
    records = parse(text)
    total = 0
    for record, counts in records:
        record, counts = unfold(record, counts)
        valid = count_valid(record, counts)
        total += valid
    return total


def is_compatible(subseq, counts):
    groups = find_groups(subseq)
    n = len(groups)
    if n > len(counts):
        return False
    if n > 0:
        # only should need to check last one really
        if groups[: n - 1] != counts[: n - 1]:
            return False
        if groups[n - 1] > counts[n - 1]:
            return False
    return True


def guided_permute(seq, counts):
    """
    >>> list(guided_permute('????.#...#...', (3, 1, 1)))[:1]
    [['#', '#', '#', '.', '.', '#', '.', '.', '.', '#', '.', '.', '.']]
    """
    indices = [i for (i, x) in enumerate(seq) if x == '?']
    seq = list(seq)
    prefixes = [[]]
    last_i = 0
    for i in indices:
        new_prefixes = []
        for subseq in prefixes:
            subseq = subseq + seq[last_i + 1 : i]
            for x in '#.':
                new_subseq = subseq + [x]
                if is_compatible(new_subseq, counts):
                    new_prefixes.append(new_subseq)
        prefixes = new_prefixes
        last_i = i
    for subseq in prefixes:
        subseq = subseq + seq[last_i + 1 :]
        if find_groups(subseq) == counts:
            yield subseq


@cache
def count_valid(seq, counts):
    # Trim off leading '.'s.
    seq = seq.lstrip('.')
    if not seq:
        return 0 if counts else 1
    if not counts:
        return 0 if ('#' in seq) else 1
    expected = counts[0]
    first_known_dot = seq.find('.')
    if first_known_dot == -1:
        first_known_dot = len(seq)
    if first_known_dot < expected:
        if '#' in seq[:first_known_dot]:
            return 0
        else:
            return count_valid(seq[first_known_dot:], counts)
    available = first_known_dot - expected + 1
    count = 0
    for j in range(available):
        x = seq[j]
        assert x in '?#', (seq, j, expected, available)
        if j + expected >= len(seq) or seq[j + expected] in '.?':
            # There needs to be a break
            n = count_valid(seq[j + expected + 1 :], counts[1:])
            count += n
        if seq[j] == '#':
            # Can't go any further since count has to start
            return count
    return count + count_valid(seq[j + 1 :], counts)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
