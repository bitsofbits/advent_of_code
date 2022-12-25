from collections import deque

example_text = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

SNAFU = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2,
}


DECIMAL = {v: k for (k, v) in SNAFU.items()}


BASE5_TO_BALANCED = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [1, -2], 4: [1, -1]}


def SNAFU_to_decimal(line):
    """
    >>> SNAFU_to_decimal("1=-0-2")
    1747
    >>> SNAFU_to_decimal("12111")
    906
    >>> SNAFU_to_decimal("2=0=")
    198
    >>> SNAFU_to_decimal("20-1-0=-2=-2220=0011")
    37503495108131
    """
    line = line.strip()
    value = 0
    for i, c in enumerate(line[::-1]):
        value += SNAFU[c] * 5**i
    return value


def reversed_base_5(n):
    if n == 0:
        return [0]
    while n:
        yield n % 5
        n //= 5


def decimal_to_SNAFU_balanced(x):
    """
    There's another way to do this based on the correspondence between
    balanced and biased number sets. If we first convert to biased
    base-5, we can then convert to balanced base-5 just by subtracting
    2 from every digit. See:

    http://homepage.divms.uiowa.edu/~jones/ternary/numbers.shtml

    >>> decimal_to_SNAFU_balanced(37503495108131)
    '20-1-0=-2=-2220=0011'
    """
    base_5 = list(reversed_base_5(x))[::-1]
    n = len(base_5) + 1
    bias = 5**n // 2
    reversed_snafu = [x - 2 for x in reversed_base_5(x + bias)]
    while reversed_snafu[-1] == 0:
        reversed_snafu.pop()
    return "".join(DECIMAL[x] for x in reversed_snafu[::-1])


def decimal_to_SNAFU(n):
    """
    >>> decimal_to_SNAFU(37503495108131)
    '20-1-0=-2=-2220=0011'
    """
    digits = deque([0])
    for i, b in enumerate(reversed_base_5(n)):
        digits.appendleft(0)
        s1, s0 = BASE5_TO_BALANCED[b]
        d = digits[1] + s0
        match d:
            case 4:
                c = 1
                d = -1
            case 3:
                c = 1
                d = -2
            case -3:
                c = -1
                d = 2
            case -4:
                c = -1
                d = 1
            case _:
                c = 0
        digits[1] = d
        digits[0] = s1 + c
    while digits[0] == 0:
        digits.popleft()
    return "".join(DECIMAL[x] for x in digits)


def part_1(text):
    """
    >>> part_1(example_text)
    '2=-1=0'
    """
    total = 0
    for line in text.strip().split("\n"):
        total += SNAFU_to_decimal(line)
    snafu = decimal_to_SNAFU(total)
    assert total == SNAFU_to_decimal(snafu), (total, SNAFU_to_decimal(snafu))
    return snafu


if __name__ == "__main__":
    import doctest

    doctest.testmod()
