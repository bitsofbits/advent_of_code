from collections import defaultdict


def parse(text):
    for line in text.strip().split("\n"):
        a, b = line.split("-")
        yield int(a), int(b)


def build_used_table(text):
    used = set()
    for a, b in parse(text):
        used.update(range(a, b + 1))
    return used


def valid_ranges(text, n_ip):
    rngs = sorted(parse(text))
    starts = [(a, 1) for (a, b) in rngs]
    ends = [(b + 1, -1) for (a, b) in rngs]
    boundmap = defaultdict(int)
    total = 0
    for i, increment in sorted(starts + ends):
        total += increment
        boundmap[i] = total
    boundmap = dict(boundmap)
    bounds = sorted(boundmap)
    for i, n in enumerate(bounds[:-1]):
        if boundmap[n] == 0:
            yield (n, bounds[i + 1])
    assert boundmap[bounds[-1]] == 0
    yield (bounds[-1], n_ip)


# def valid_ip(text, n_ip):
#     for x in valid_ranges(text, n_ip):
#         print(x)

#     used_ranges = sorted(parse(text))
#     range_keys = [a for (a, b) in used_ranges]
#     rangemap = {}
#     for a in sorted(set(a for (a, b) in used_ranges)):
#         j = bisect_right(range_keys, a)
#         rangemap[j] = sorted(used_ranges[:j], key=lambda x: x[1])

#     for i in range(n_ip):
#         j = bisect_right(range_keys, i)
#         rngs = rangemap[j]
#         k = bisect_left(rngs, i, key=lambda x: x[1])
#         for a, b in rngs[k:]:
#             if i >= a and i <= b:
#                 break
#         else:
#             yield i


def part_1(text, n_ip=4294967296):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """
    for (a, b) in valid_ranges(text, n_ip):
        return a


def part_2(text, n_ip=4294967296):
    """
    >>> part_2(EXAMPLE_TEXT, n_ip=10)
    2
    """
    cnt = 0
    for (a, b) in valid_ranges(text, n_ip):
        cnt += b - a
    return cnt


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
