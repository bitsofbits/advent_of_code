from functools import cache
from math import log2


def parse_line(x):
    x = x.strip()
    if x == 'deal into new stack':
        return ('invert', None)
    x, arg = x.rsplit(maxsplit=1)
    arg = int(arg)
    if x == 'deal with increment':
        return ('deal', arg)
    if x == 'cut':
        return ('cut', arg)
    raise ValueError(x)


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:5]
    [('invert', None), ('cut', -2), ('deal', 7), ('cut', 8), ('cut', -4)]
    """
    return [parse_line(x) for x in text.strip().split('\n')]


def invert(x, _):
    return x[::-1]


def cut(x, n):
    return x[n:] + x[:n]


def deal(x, n):
    n_cards = len(x)
    new_x = [None] * n_cards
    for i in range(n_cards):
        new_x[(i * n) % n_cards] = x[i]
    return new_x
    # return [x[(i * n) % n_cards] for i in range(n_cards)]


command_map = {'invert': invert, 'cut': cut, 'deal': deal}


# def mod_inverse(
#     pow(b, m - 2, m))


def symbolic_apply(n, commands):
    a = 1
    b = 0
    for cmd, arg in commands[::-1]:
        match cmd:
            case 'invert':  # n  - 1 - (a i + b)
                a = -a
                b = (n - 1) - b
            case 'cut':
                b = b + arg
            case 'deal':  # arg * (i1 + b1)  =  (a i + b)
                inv = pow(arg, n - 2, n)
                a = inv * a
                b = inv * b
            case _:
                raise ValueError(cmd)
    return a, b


def apply_to(cards, commands, symbolic=False):
    """
    >>> cards = list(range(10))
    >>> commands = parse(EXAMPLE_TEXT)
    >>> apply_to(cards, commands)
    [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    >>> commands = parse(EXAMPLE2_TEXT)
    >>> apply_to(cards, commands)
    [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
    >>> commands = parse(EXAMPLE3_TEXT)
    >>> apply_to(cards, commands)
    [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    """
    if not symbolic:
        for cmd, arg in commands:
            cards = command_map[cmd](cards, arg)
        return cards
    else:
        n = len(cards)
        a, b = symbolic_apply(n, commands)
        return [cards[(a * i + b) % n] for i in range(n)]


def part_1(text, n_cards=10007):
    """
    >>> part_1(INPUT_TEXT)
    8191
    """
    # 1545 is too low
    # cards = list(range(n_cards))
    # cards = apply_to(cards, parse(text), symbolic=True)
    # for i, x in enumerate(cards):
    #     if x == 2019:
    #         return i
    a, b = symbolic_apply(n_cards, parse(text))
    for i in range(n_cards):
        if (a * i + b) % n_cards == 2019:
            return i


# def part_2(text, n_cards=119315717514047, n_repeats=101741582076661):
#     """
#     >>> part_2(INPUT_TEXT)


#     80761411424761 is too high
#     """
#     commands = parse(text)
#     a, b = symbolic_apply(n_cards, commands)
#     a = (a * n_repeats) % n_cards
#     b = (b * n_repeats) % n_cards
#     return (a * 2020 + b) % n_cards


@cache
def mult(a1, b1, a2, b2, n):
    # a2 * (a1 * i + b1) + b2
    return (a1 * a2) % n, (a2 * b1 + b2) % n
    # a0 ** n, b0 * (1 + a + )


@cache
def recursive_power(a, b, p, n):
    if n == 1:
        return a, b
    else:
        best_n = 2 ** int(log2(n))
        n1 = best_n // 2
        a1, b1 = recursive_power(a, b, p, n1)
        a1, b1 = mult(a1, b1, a1, b1, p)
        n2 = n - 2 * n1
        if n2:
            a2, b2 = recursive_power(a, b, p, n2)
            a1, b1 = mult(a1, b1, a2, b2, p)
        return a1, b1


def part_2(text, n_cards=119315717514047, n_repeats=101741582076661):
    """
    >>> part_2(INPUT_TEXT)

    80761411424761 is too high
    """
    commands = parse(text)
    a0, b0 = symbolic_apply(n_cards, commands)
    a, b = recursive_power(a0, b0, n_cards, n_repeats)
    # a, b = 1, 0
    # a = pow(a0, n_repeats, n_cards)

    # for _ in range(n_repeats):
    #     b = (a0 * b + b0) % n_cards
    return (a * 2020 + b) % n_cards


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "example3.txt") as f:
        EXAMPLE3_TEXT = f.read()
    doctest.testmod()
