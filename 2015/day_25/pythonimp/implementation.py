def generate_codes():
    """
    >>> for _, x in zip(range(3), generate_codes()): pass
    >>> x
    (1, 2, 18749137)
    """
    x = 20151125
    i = j = 0
    while True:
        yield i + 1, j + 1, x
        x = (x * 252533) % 33554393
        i -= 1
        j += 1
        if i < 0:
            i = j
            j = 0


def part_1(text):
    """ """
    for row, col, code in generate_codes():
        if (row, col) == (2947, 3029):
            return code


def part_2(text):
    """ """
    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()
