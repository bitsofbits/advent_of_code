from collections import Counter


def parse_line(line):
    line = line.strip()
    name, rest = line.rsplit("-", 1)
    sector_id, checksum = rest[:-1].split("[")
    return name, int(sector_id), checksum


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [('aaaaa-bbb-z-y-x', 123, 'abxyz'), ('a-b-c-d-e-f-g-h', 987, 'abcde')]
    """
    for line in text.strip().split("\n"):
        yield parse_line(line)


def compute_checksum(name):
    counts = Counter(name.replace("-", "")).most_common()
    counts.sort(key=lambda x: (-x[1], x[0]))
    return "".join(c for (c, cnt) in counts[:5])


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1514
    """
    total = 0
    for name, sid, checksum in parse(text):
        if checksum == compute_checksum(name):
            total += sid
    return total


def decode_word(word, sector_id):
    return "".join([chr((ord(x) - ord("a") + sector_id) % 26 + ord("a")) for x in word])


def decode(name, sector_id):
    """
    >>> decode("qzmt-zixmtkozy-ivhz", 343)
    'very encrypted name'
    """
    return " ".join(decode_word(x, sector_id) for x in name.split("-"))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    for encrypted, sid, checksum in parse(text):
        if checksum == compute_checksum(encrypted):
            name = decode(encrypted, sid)
            if "pole" in name:
                return sid


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
