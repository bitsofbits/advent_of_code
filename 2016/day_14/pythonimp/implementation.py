import re
from collections import deque
from hashlib import md5
from itertools import count

# md5(text).hexdigest()


def hashof(i, seed, stretch):
    text = f"{seed}{i}"
    for _ in range(stretch + 1):
        text = md5(text.encode("ascii")).hexdigest()
    return text


def generate_codes(seed, stretch=0):
    """
    >>> seed = parse(EXAMPLE_TEXT)
    >>> items = list(x for (i, x) in zip(range(64), generate_codes(seed)))
    >>> [x[0] for x in items[:2]]
    [39, 92]
    >>> items[-1][0]
    22728
    """
    hashes = deque()
    triple = re.compile(r"(.)\1\1")
    # quintuple = re.compile(r"(.)\1\1\1\1")
    for i in count():
        if not len(hashes):
            hashes.append(hashof(i, seed, stretch))
        candidate = hashes.popleft()
        if (m := triple.search(candidate)) is not None:
            target = m.group(1) * 5
            for j in range(1000):
                if len(hashes) == j:
                    hashes.append(hashof(i + j + 1, seed, stretch))
                # if (m := quintuple.search(hashes[j])) and m.group(1) == target:
                if target in hashes[j]:
                    yield i, candidate, target
                    break


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    'abc'
    """
    return text.strip()


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT) # 12292 is too low also 12291 ???
    22728
    """
    seed = parse(text)
    items = list(x for (i, x) in zip(range(64), generate_codes(seed)))
    return items[-1][0]


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    22551
    """
    seed = parse(text)
    items = list(x for (i, x) in zip(range(64), generate_codes(seed, stretch=2016)))
    return items[-1][0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
