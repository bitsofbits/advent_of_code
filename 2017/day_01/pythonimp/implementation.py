def part_1(text):
    """
    >>> part_1("1122")
    3
    >>> part_1("1111")
    4
    """
    text = text.strip()
    n = len(text)
    return sum(int(x) for (i, x) in enumerate(text) if x == text[(i + 1) % n])


def part_2(text):
    """
    >>> part_2("1212")
    6
    >>> part_2("1221")
    0
    >>> part_2("12131415")
    4
    """
    text = text.strip()
    n = len(text)
    di = n // 2
    return sum(int(x) for (i, x) in enumerate(text) if x == text[(i + di) % n])


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    doctest.testmod()
