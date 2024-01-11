def parse(text):
    """
    >>> parse(INPUT_TEXT)
    (307237, 769058)
    """
    return tuple(int(x) for x in text.split('-'))


one_less_than_1 = chr(ord('1') - 1)


def is_valid(number_string):
    """
    >>> is_valid("111111")
    True
    >>> is_valid("223450")
    False
    >>> is_valid("223450")
    False
    """
    if len(number_string) != 6:
        return False
    last = one_less_than_1
    has_double = False
    for x in number_string:
        if x not in '1234567890':
            return False
        if x < last:
            return False
        if x == last:
            has_double = True
        last = x
    return has_double


def find_valid(low, high):
    valid = []
    for i in range(low, high + 1):
        if is_valid(str(i)):
            valid.append(i)
    return valid


def part_1(text):
    """
    >>> part_1(INPUT_TEXT)
    889
    """
    low, high = parse(text)
    return len(find_valid(low, high))


def is_valid_2(number_string):
    """
    >>> is_valid_2("112233")
    True
    >>> is_valid_2("123444")
    False
    >>> is_valid_2("111122")
    True

    """
    if len(number_string) != 6:
        return False
    last = one_less_than_1
    has_double = False
    potential_double_length = 0
    for x in number_string:
        if x not in '1234567890':
            return False
        if x < last:
            return False
        potential_double_length += 1
        if x != last:
            if potential_double_length == 2:
                has_double = True
            potential_double_length = 0
        last = x
    potential_double_length += 1
    if potential_double_length == 2:
        has_double = True
    return has_double


def find_valid_2(low, high):
    valid = []
    for i in range(low, high + 1):
        if is_valid_2(str(i)):
            valid.append(i)
    return valid


def part_2(text):
    """
    >>> part_2(INPUT_TEXT)
    589
    """
    low, high = parse(text)
    return len(find_valid_2(low, high))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
