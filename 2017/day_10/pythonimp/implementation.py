from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [3, 4, 1, 5]
    """
    return [int(x) for x in text.strip().split(",")]


def knot_hash(hashlen, lengths, rounds=1):
    values = deque(range(hashlen))
    start = 0
    skip = 0
    for _ in range(rounds):
        for n in lengths:
            assert n <= hashlen
            # Start of reversed is always at zero
            chunk = [values.popleft() for _ in range(n)]
            for x in chunk:
                values.appendleft(x)
            # Now shift to put start in the correct place
            delta = n + skip
            values.rotate(-delta)
            start = (start + delta) % hashlen
            skip = (skip + 1) % hashlen
    # We've rotated start to the left
    values.rotate(start)
    return values


def part_1(text, hashlen=256):
    """
    >>> part_1(EXAMPLE_TEXT, 5)
    12
    """
    hashed = knot_hash(hashlen, parse(text))
    return hashed[0] * hashed[1]


def part_2(text):
    """
    >>> part_2("")
    'a2582a3a0e66e6e86e3812dcb672a272'
    >>> part_2("AoC 2017")
    '33efeb34ea91902bb2f59c9920caa6cd'
    >>> part_2("1,2,3")
    '3efbe78a8d82f29979031a4aa0b16a9d'
    >>> part_2("1,2,4")
    '63960835bcdc130f0b66d7ff4f6a5a8e'
    """
    # Oh wait, bytes you say!
    lengths = [ord(x) for x in text.strip()]
    # And add some extra, why not?
    lengths += [17, 31, 73, 47, 23]
    # print(lengths)
    hashed = knot_hash(256, lengths, rounds=64)
    # print(hashed)
    # Sparsify
    digest = ""
    for i in range(0, 256, 16):
        xor = hashed[i]
        for j in range(i + 1, i + 16):
            xor ^= hashed[j]
        digest += f"{xor:02x}"
    return digest


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
