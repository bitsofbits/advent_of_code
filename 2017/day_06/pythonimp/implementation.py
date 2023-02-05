from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [0, 2, 7, 0]
    """
    return [int(x) for x in text.strip().split()]


def find_loop(text):
    blocks = [(x, i) for (i, x) in enumerate(parse(text))]
    n_blocks = len(blocks)
    seen = {tuple(blocks): 0}
    for step in count(1):
        i = max(blocks, key=lambda x: (x[0], -x[1]))[1]
        n = blocks[i][0]
        blocks[i] = (0, i)
        for j in range(n):
            i1 = (i + j + 1) % n_blocks
            blocks[i1] = (blocks[i1][0] + 1, i1)
        key = tuple(blocks)
        if key in seen:
            return seen[key], step
        seen[key] = step


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)   # 1837 too low?
    5
    """
    first_seen, first_repeat = find_loop(text)
    return first_repeat


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    4
    """
    first_seen, first_repeat = find_loop(text)
    return first_repeat - first_seen


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
