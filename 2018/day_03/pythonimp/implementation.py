from collections import defaultdict


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))
    [('#1', (1, 3), (4, 4)), ('#2', (3, 1), (4, 4)), ('#3', (5, 5), (2, 2))]

    """
    for line in text.strip().split('\n'):
        id_, rest = line.split(' @ ')
        corner, size = rest.split(': ')
        left, top = (int(x) for x in corner.split(','))
        width, height = (int(x) for x in size.split('x'))
        yield id_, (left, top), (width, height)


def get_claim_counts(claims):
    fabric = defaultdict(int)
    for _, (left, top), (width, height) in claims:
        for i in range(left, left + width):
            for j in range(top, top + height):
                fabric[i, j] += 1
    return fabric


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4
    """
    claim_counts = get_claim_counts(parse(text))
    return sum((v > 1) for v in claim_counts.values())


def overlaps(claim_counts, claim):
    _, (left, top), (width, height) = claim
    for i in range(left, left + width):
        for j in range(top, top + height):
            if claim_counts[i, j] > 1:
                return True
    return False


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    '#3'
    """
    claims = list(parse(text))
    claim_counts = get_claim_counts(claims)
    for claim in claims:
        id_, *_ = claim
        if not overlaps(claim_counts, claim):
            return id_


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
