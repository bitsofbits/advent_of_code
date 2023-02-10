from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    """


def knot_hash(seed, hashlen=256, rounds=64):
    lengths = [ord(x) for x in seed] + [17, 31, 73, 47, 23]
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
    # densify
    digest = ""
    for i in range(0, 256, 16):
        xor = values[i]
        for j in range(i + 1, i + 16):
            xor ^= values[j]
        digest += f"{xor:02x}"
    return digest


def compute_grid(seed):
    """
    >>> n = int("a0c20170", base=16)
    >>> f"{n:0128b}"[-32:]
    '10100000110000100000000101110000'

    >>> for x in list(compute_grid(EXAMPLE_TEXT))[:8]: print(x[:8])
    11010100
    01010101
    00001010
    10101101
    01101000
    11001001
    01000100
    11010110
    """
    seed = seed.strip()
    for i in range(128):
        khash = knot_hash(f"{seed}-{i}")
        n = int(khash, base=16)
        yield f"{n:0128b}"


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    8108
    """
    used = 0
    for row in compute_grid(text):
        used += sum(1 for x in row if x == "1")
    return used


def find_one_island(board, seen):
    for x in board:
        if x not in seen:
            break
    else:
        raise ValueError("no valid starting places")

    stack = [x]
    island = set([x])

    while stack:
        i, j = stack.pop()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            p = (i + di, j + dj)
            if p not in board:
                continue
            if p in island:
                continue
            stack.append(p)
            island.add(p)
    return island


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1242
    """
    board = set()
    for i, row in enumerate(compute_grid(text)):
        for j, c in enumerate(row):
            if c == "1":
                board.add((i, j))
    board = frozenset(board)

    seen = set()
    count = 0
    while len(seen) < len(board):
        seen |= find_one_island(board, seen)
        count += 1
    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
