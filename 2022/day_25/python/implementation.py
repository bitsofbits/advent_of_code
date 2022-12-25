from itertools import count

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


B5 = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [1, -2], 4: [1, -1]}


"""
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37
"""


def SNAFU_to_decimal(line):
    """
    >>> SNAFU_to_decimal("1=-0-2")
    1747
    >>> SNAFU_to_decimal("12111")
    906
    >>> SNAFU_to_decimal("2=0=")
    198
    """
    line = line.strip()
    value = 0
    for i, c in enumerate(line[::-1]):
        value += SNAFU[c] * 5**i
    return value


def base_5(n):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % 5))
        n //= 5
    return digits[::-1]


def decimal_to_SNAFU(n):
    b5 = base_5(n)
    digits = [0] * (len(b5) + 1)
    n = len(b5)
    for i, b in enumerate(b5[::-1]):
        s1, s0 = B5[b]
        d = digits[n - i] + s0
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
        digits[n - i] = d
        digits[n - (i + 1)] = s1 + c
    while digits[0] == 0:
        digits = digits[1:]
    return "".join([DECIMAL[x] for x in digits])


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
