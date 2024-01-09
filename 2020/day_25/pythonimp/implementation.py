from itertools import count


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [5764801, 17807724]
    """
    return [int(x) for x in text.split()]


def hash_step(x, subject_number):
    return (x * subject_number) % 20201227


def find_loop_size(public_key):
    """
    >>> a, b = parse(EXAMPLE_TEXT)
    >>> find_loop_size(a)
    8
    >>> find_loop_size(b)
    11
    """
    x = 1
    for i in count():
        if x == public_key:
            return i
        x = hash_step(x, 7)


def hash(subject_number, loop_size):
    x = 1
    for _ in range(loop_size):
        x = hash_step(x, subject_number)
    return x


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    14897079
    """
    a, b = parse(text)
    loop_size_a = find_loop_size(a)
    encryption_key = hash(b, loop_size_a)
    return encryption_key


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
