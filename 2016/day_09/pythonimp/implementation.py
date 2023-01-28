# A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
# (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker, it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
# X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further.


def decode(x):
    """
    >>> decode("ADVENT")
    'ADVENT'
    >>> decode("A(1x5)BC")
    'ABBBBBC'
    >>> decode("(3x3)XYZ")
    'XYZXYZXYZ'
    >>> decode("A(2x2)BCD(2x2)EFG ")
    'ABCBCDEFEFG'
    >>> decode("(6x1)(1x3)A")
    '(1x3)A'
    >>> decode("X(8x2)(3x3)ABCY")
    'X(3x3)ABC(3x3)ABCY'
    """
    x = x.replace(" ", "")
    i1 = 0
    chunks = []
    while True:
        i0 = x.find("(", i1)
        if i0 == -1:
            break
        chunks.append(x[i1:i0])
        i1 = x.find(")", i0)
        a, b = (int(x) for x in x[i0 + 1 : i1].split("x"))
        chunks.extend([x[i1 + 1 : i1 + 1 + a] * b])
        i1 = i1 + a + 1
    chunks.append(x[i1:])
    return "".join(chunks)


def part_1(text):
    return len(decode(text))


def recursive_decode(text):
    """
    >>> recursive_decode("(3x3)XYZ")
    'XYZXYZXYZ'
    >>> recursive_decode("X(8x2)(3x3)ABCY")
    'XABCABCABCABCABCABCY'
    >>> len(recursive_decode("(27x12)(20x12)(13x14)(7x10)(1x12)A"))
    241920
    """
    while "(" in text:
        text = decode(text)
    return text


def decoded_length(x):
    """
    >>> decoded_length("(3x3)XYZ")
    9
    >>> decoded_length("X(8x2)(3x3)ABCY")
    20
    >>> decoded_length("(27x12)(20x12)(13x14)(7x10)(1x12)A")
    241920
    >>> decoded_length("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN")
    445
    """
    x = x.replace(" ", "")
    i1 = 0
    length = 0
    while True:
        i0 = x.find("(", i1)
        if i0 == -1:
            break
        length += i0 - i1
        i1 = x.find(")", i0)
        a, b = (int(x) for x in x[i0 + 1 : i1].split("x"))
        length += b * decoded_length(x[i1 + 1 : i1 + 1 + a])
        i1 = i1 + a + 1
    length += len(x) - i1
    return length


def part_2(text):
    return decoded_length(text)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
