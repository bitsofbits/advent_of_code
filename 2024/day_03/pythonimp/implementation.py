import re


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    161
    """
    pattern = re.compile(r'mul\((\d*),(\d*)\)')
    return sum(int(a) * int(b) for (a, b) in pattern.findall(text))


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    48
    """
    pattern = re.compile(r'((mul)\((\d*),(\d*)\))|(do\(\))|(don\'t\(\))')
    multiply = True
    total = 0
    for _, _, a, b, do, do_not in pattern.findall(text):
        if do:
            multiply = True
        elif do_not:
            multiply = False
        elif multiply:
            total += int(a) * int(b)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example_2.txt") as f:
        EXAMPLE2_TEXT = f.read()

    doctest.testmod()
