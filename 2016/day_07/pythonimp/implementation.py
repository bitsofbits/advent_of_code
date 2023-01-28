import re


def parse_address(line):
    line = line.strip()
    oob = []
    inb = []
    while "[" in line:
        x, line = line.split("[", 1)
        oob.append(x)
        assert "]" in line
        x, line = line.split("]", 1)
        inb.append(x)
    oob.append(line)
    return oob, inb


abba_pattern = re.compile(r"(.)(.)\2\1")


def has_abba(x):
    """
    >>> has_abba("abba")
    True
    >>> has_abba("aaaa")
    False
    >>> has_abba("abcde")
    False

    """
    return any(len(set(y)) == 2 for y in abba_pattern.findall(x))


def supports_tls(address):
    """
    >>> [supports_tls(x) for x in EXAMPLE_TEXT.strip().split("\\n")]
    [True, False, False, True]
    """
    oob, inb = parse_address(address)
    return any(has_abba(x) for x in oob) and not any(has_abba(x) for x in inb)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    count = 0
    for address in text.strip().split("\n"):
        address = address.strip()
        if supports_tls(address):
            count += 1
    return count


aba_pattern = re.compile(r"(.)(.)\1")


def extract_abas(x):
    abas = set()
    start = 0
    while True:
        m = aba_pattern.search(x, start)
        if m is None:
            break
        a, b = m.group(1, 2)
        if a != b:
            abas.add((a, b))
        start = m.start() + 1
    return abas


EXAMPLE2_TEXT = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
"""


def supports_ssl(address):
    """
    >>> [supports_ssl(x) for x in EXAMPLE2_TEXT.strip().split("\\n")]
    [True, False, True, True]
    """
    oob, inb = parse_address(address)
    abas = set()
    for x in oob:
        abas.update(extract_abas(x))
    babs = set()
    for x in abas:
        a, b = x
        babs.add((b, a))
    for x in inb:
        if set(extract_abas(x)) & babs:
            return True
    return False


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    3
    """
    count = 0
    for address in text.strip().split("\n"):
        address = address.strip()
        if supports_ssl(address):
            count += 1
    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
