from collections import defaultdict
from functools import cache


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    ('mask', 66, 64)
    ('mem', 8, 11)
    ('mem', 7, 101)
    ('mem', 8, 0)
    """
    for line in text.strip().split("\n"):
        if line.startswith("mem"):
            line, val = line.split(" = ")
            _, loc = line[:-1].split("[")
            yield "mem", int(loc), int(val)
        elif line.startswith("mask"):
            _, val = line.split(" = ")
            msk = int(val.replace("0", "1").replace("X", "0"), base=2)
            val = int(val.replace("X", "0"), base=2)
            yield "mask", msk, val


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    165
    """
    registers = defaultdict(int)
    mask_msk = None
    mask_val = None
    for cmd in parse(text):
        match cmd:
            case "mask", msk, val:
                mask_msk = msk
                mask_val = val
            case "mem", loc, val:
                registers[loc] = (val & ~mask_msk) | mask_val
            case _:
                raise ValueError(cmd)
    return sum(registers.values())


@cache
def bitsof(x):
    bits = []
    for i in range(36):
        if x & 1 == 0:
            bits.append(i)
        x >>= 1
    bits.reverse()
    return bits


@cache
def masksof(x):
    # Iterate over possible masks by counting
    # and then choosing matching masks values.
    # Not super efficient but fast enough for this.
    masks = []
    bits = bitsof(x)
    n = 2 ** len(bits)
    for i in range(n):
        v = 0
        for j in range(36):
            if i & 1:
                v |= 2 ** bits[j]
            i >>= 1
            if not i:
                break
        masks.append(v)
    return masks


def decode(loc, msk, val):
    loc |= val

    masks = masksof(msk)
    mask_msk = masks[-1]
    for m in masks:
        yield (loc & ~mask_msk) | m


EXAMPLE2_TEXT = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    208
    """
    registers = defaultdict(int)
    mask_msk = None
    mask_val = None
    for cmd in parse(text):
        match cmd:
            case "mask", msk, val:
                mask_msk = msk
                mask_val = val
            case "mem", loc, val:
                for x in decode(loc, mask_msk, mask_val):
                    registers[x] = val
            case _:
                raise ValueError(cmd)
    return sum(registers.values())


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
