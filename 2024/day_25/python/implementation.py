
def parse(text):
    """
    >>> keys, locks = parse(EXAMPLE_TEXT)
    >>> for x in locks: print(x)
    (0, 5, 3, 4, 3)
    (1, 2, 0, 5, 3)

    >>> for x in keys: print(x)
    (5, 0, 2, 1, 3)
    (4, 3, 4, 0, 2)
    (3, 0, 2, 0, 1)
    """
    keys = []
    locks = []
    for block in text.strip().split('\n\n'):
        if block.startswith('.....\n'):
            key = [5] * 5
            for i, row in enumerate(block.strip().split('\n')):
                for j, x in enumerate(row):
                    if x == '.':
                        h = 5 - i
                        key[j] = min(h, key[j])
                assert j == 4, j
            assert i == 6, i
            keys.append(tuple(key))
        elif block.startswith('#####\n'):
            lock = [0] * 5
            for i, row in enumerate(block.strip().split('\n')):
                for j, x in enumerate(row):
                    if x == '#':
                        lock[j] = max(i, lock[j])
                assert j == 4, j
            assert i == 6, i
            locks.append(tuple(lock))
        else:
            raise ValueError(block)

    return keys, locks



def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    keys, locks = parse(text)

    # Ensure no duplicates
    assert len(set(keys)) == len(keys)
    assert len(set(locks)) == len(locks)

    count = 0
    for K in keys:
        for L in locks:
            for a, b in zip(K, L):
                if a + b > 5:
                    break
            else:
                count += 1

    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
