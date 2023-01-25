from hashlib import md5
from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    'abc'
    """
    return text.strip()


def next(door_id, n):
    for i in count(n):
        digest = md5(f"{door_id}{i}".encode("ascii")).hexdigest()
        if digest.startswith("00000"):
            return i, digest[5], digest[6]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    '18f47a30'
    """
    n = -1
    door_id = parse(text)
    password = []
    for _ in range(8):
        n, c, _ = next(door_id, n + 1)
        password.append(c)
    return "".join(password)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    '05ace8e3'
    """
    n = -1
    door_id = parse(text)
    password = [None] * 8
    while None in password:
        n, p, c = next(door_id, n + 1)
        if not ("0" <= p < "8"):
            continue
        p = int(p)
        if password[p] is None:
            password[p] = c
    return "".join(password)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
