# Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example, s3 on abcde produces cdeab).
# Exchange, written xA/B, makes the programs at positions A and B swap places.
# Partner, written pA/B, makes the programs named A and B swap places.
from itertools import count


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('s', 1)
    ('x', 3, 4)
    ('p', 'e', 'b')
    """
    for cmd in text.strip().split(","):
        parts = cmd[:1], *(cmd[1:].split("/"))
        match parts:
            case "s", n:
                yield "s", int(n)
            case "x", i, j:
                yield "x", int(i), int(j)
            case "p", a, b:
                yield "p", a, b
            case _:
                raise ValueError(parts)


def dance_once(p, commands):
    for cmd in commands:
        match cmd:
            case "s", n:
                assert n > 0
                p = p[-n:] + p[:-n]
            case "x", i, j:
                p[i], p[j] = p[j], p[i]
            case "p", a, b:
                i = p.index(a)
                j = p.index(b)
                p[i], p[j] = p[j], p[i]
            case _:
                raise ValueError(cmd)
    return p


def part_1(text, cnt=16):
    """
    >>> part_1(EXAMPLE_TEXT, 5)
    'baedc'
    """
    p = [chr(ord("a") + i) for i in range(cnt)]
    commands = parse(text)
    p = dance_once(p, commands)
    return "".join(p)


def part_2(text, cnt=16):
    p = [chr(ord("a") + i) for i in range(cnt)]
    commands = list(parse(text))
    states = {tuple(p): 0}
    target = 1_000_000_000
    for i in count():
        if i >= target:
            break
        p = dance_once(p, commands)
        k = tuple(p)
        if k in states:
            period = i - states[k]
            target = i + (target - i) % 60
        states[k] = i
    return "".join(p)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
