def binarize(text):
    """
    >>> binarize("D2FE28")
    '110100101111111000101000'
    """
    binary = []
    for x in text.strip():
        x = int(x, 16)
        binary.extend(x for x in f"{x:04b}")
    return "".join(binary)


def parse_literal(x):
    chunks = []
    while x:
        leading_bit = x[0]
        chunks.append(x[1:5])
        x = x[5:]
        if leading_bit == "0":
            break
    value = int("".join(chunks), 2)
    return value, x


def parse_by_length(x):
    """
    >>> parse("38006F45291200")
    ((1, 6, [(6, 4, 10), (2, 4, 20)]), '0000000')
    """
    assert x[0] == "0"
    n = int(x[1:16], 2)
    extra = x[16 + n :]
    x = x[16 : 16 + n]
    payloads = []
    while x:
        data, x = parse_bin(x)
        payloads.append(data)
    return payloads, extra


def parse_by_count(x):
    """
    >>> parse("EE00D40C823060")
    ((7, 3, [(2, 4, 1), (4, 4, 2), (1, 4, 3)]), '00000')
    """
    assert x[0] == "1"
    n = int(x[1:12], 2)
    x = x[12:]
    payloads = []
    for _ in range(n):
        data, x = parse_bin(x)
        payloads.append(data)
    return payloads, x


def parse_bin(x):
    version = int(x[:3], 2)
    type_id = int(x[3:6], 2)
    payload = x[6:]
    match type_id, payload[0]:
        case 4, _:
            payload, extra = parse_literal(payload)
        case _, "0":
            payload, extra = parse_by_length(payload)
        case _, "1":
            payload, extra = parse_by_count(payload)
        case _:
            raise ValueError()

    return (version, type_id, payload), extra


def parse(text):
    """
    >>> parse("D2FE28")
    ((6, 4, 2021), '000')
    """
    b = binarize(text)

    return parse_bin(b)


def extract_version_nums(x):
    v, _, p = x
    yield v
    if isinstance(p, list):
        for x in p:
            yield from extract_version_nums(x)


def part_1(text):
    """
    >>> part_1("EE00D40C823060")
    14
    """
    data, extra = parse(text)
    return sum(extract_version_nums(data))


def prod(values):
    v = 1
    for x in values:
        v *= x
    return v


def eval(x):
    _, tid, p = x
    match tid:
        case 0:
            return sum(eval(x) for x in p)
        case 1:
            return prod(eval(x) for x in p)
        case 2:
            return min(eval(x) for x in p)
        case 3:
            return max(eval(x) for x in p)
        case 4:
            return p
        case 5:
            a, b = (eval(x) for x in p)
            return a > b
        case 6:
            a, b = (eval(x) for x in p)
            return a < b
        case 7:
            a, b = (eval(x) for x in p)
            return a == b
        case _:
            raise ValueError()


def part_2(text):
    """
    >>> part_2("C200B40A82")
    3
    >>> part_2("04005AC33890")
    54
    >>> part_2("880086C3E88112")
    7
    """
    data, extra = parse(text)
    return eval(data)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
