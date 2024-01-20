from collections import Counter, defaultdict


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:4]
    ['abcdef', 'bababc', 'abbcde', 'abcccd']
    """
    for line in text.strip().split():
        yield line


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    12
    """
    repeats_2x_cnt = 0
    repeats_3x_cnt = 0
    for id_ in parse(text):
        counts = Counter(id_).most_common()
        for k, n in counts:
            if n == 2:
                repeats_2x_cnt += 1
                break
            if n < 2:
                break
        for k, n in counts:
            if n == 3:
                repeats_3x_cnt += 1
                break
            if n < 3:
                break

    return repeats_2x_cnt * repeats_3x_cnt


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    'fgij'
    """
    ids = list(parse(text))
    id_length = len(ids)
    for i in range(id_length):
        fingerprints = set()
        for id_ in ids:
            fingerprint = id_[:i] + id_[i + 1 :]
            if fingerprint in fingerprints:
                return fingerprint
            else:
                fingerprints.add(fingerprint)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
