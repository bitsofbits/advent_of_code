import random
from collections import deque
from math import sqrt

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


SNAFU_DIGITS = "=-012"


def _score(snafu, decimal):
    return (SNAFU_to_decimal(snafu) - decimal) ** 2


def clip(x, low, high):
    if x < low:
        return low
    if x > high:
        return high
    return x


def _mutate(x, score):
    n = 1
    while 5 ** (n + 1) // 2 < sqrt(score):
        n += 1
    x = list(x)
    mutations = random.randrange(len(x) + 1) + 1
    for _ in range(mutations):
        if not x:
            x.append(random.choice(SNAFU_DIGITS))
            continue
        # Change length at most 10% of the time
        match random.randrange(mutations + 18):
            case 0:
                i = random.randrange(len(x) + 1)
                x.insert(i, random.choice(SNAFU_DIGITS))
            case 1:
                i = random.randrange(len(x))
                x.pop(i)
            case _:
                focus = len(x) - n - 1
                i = int(clip(random.gauss(focus, 1.0), 0, len(x) - 1))
                x[i] = random.choice(SNAFU_DIGITS)
    return "".join(x)


def _normalize(x):
    while x[:1] == "0":
        x = x[1:]
    if x == "":
        x = "0"
    return x


def decimal_to_SNAFU_beam(n, candidates=10, offspring=10):
    """Find SNAFU using a beam search

    A cool idea I got from flowblok@tech.lgbt in
    https://tech.lgbt/@flowblok/109578526233453752

    I tweaked this to focus on the regions that correspond
    to the current score (see _mutate). I also do more
    mutations on longer sequences. These two modifications
    sped it up a lot for my case. Still a lot slower
    than computing it deterministically, but perhaps
    more generally useful.

    >>> decimal_to_SNAFU_beam(37503495108131)
    '20-1-0=-2=-2220=0011'
    >>> decimal_to_SNAFU_beam(198)
    '2=0='
    >>> decimal_to_SNAFU_beam(62)
    '222'
    >>> decimal_to_SNAFU_beam(63)
    '1==='
    >>> decimal_to_SNAFU_beam(0)
    '0'
    """
    beam = {"0": _score("0", n)}
    while True:
        keys = sorted(beam, key=lambda x: beam[x])[:candidates]
        if beam[keys[0]] == 0:
            return _normalize(keys[0])
        for k in keys:
            for i in range(offspring):
                if (x := _mutate(k, beam[k])) not in beam:
                    beam[x] = _score(x, n)


def decimal_to_SNAFU_balanced(n):
    """
    Convert from decimal to SNAFU using the correspondence between
    balanced and biased number sets. If we first convert to biased
    base-5, we can then convert to balanced base-5 just by subtracting
    2 from every digit. See:

    http://homepage.divms.uiowa.edu/~jones/ternary/numbers.shtml

    >>> decimal_to_SNAFU_balanced(37503495108131)
    '20-1-0=-2=-2220=0011'
    >>> decimal_to_SNAFU_balanced(198)
    '2=0='
    >>> decimal_to_SNAFU_balanced(62)
    '222'
    >>> decimal_to_SNAFU_balanced(63)
    '1==='
    >>> decimal_to_SNAFU_balanced(0)
    '0'
    """
    rng = 5
    while rng // 2 < abs(n):
        rng *= 5
    n += rng // 2
    balaced = [n % 5]
    while n := n // 5:
        balaced.append(n % 5)
    return "".join("=-012"[x] for x in balaced[::-1])


def reversed_base_5(n):
    if n == 0:
        return [0]
    while n:
        yield n % 5
        n //= 5


BASE5_TO_BALANCED = {0: [0, 0], 1: [0, 1], 2: [0, 2], 3: [1, -2], 4: [1, -1]}
DECIMAL_TO_SNAFU = {v: k for (k, v) in SNAFU.items()}


def decimal_to_SNAFU(n):
    """
    >>> decimal_to_SNAFU(37503495108131)
    '20-1-0=-2=-2220=0011'
    """
    digits = deque([0])
    for b5 in reversed_base_5(n):
        digits.appendleft(0)
        s1, s0 = BASE5_TO_BALANCED[b5]
        d = digits[1] + s0
        match d:
            case 3 | 4:
                c = 1
            case -3 | -4:
                c = -1
            case _:
                c = 0
        digits[1] = d - c * 5
        digits[0] = s1 + c
    while digits[0] == 0:
        digits.popleft()
    return "".join(DECIMAL_TO_SNAFU[x] for x in digits)


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
