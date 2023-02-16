from collections import defaultdict


def parse_chunk(x):
    x = x.strip()
    x, _ = x.rsplit(" ", 1)
    n, kind = x.split(" ", 1)
    return int(n), kind


def parse(text):
    for line in text.strip().split("\n"):
        outer, rest = line.split(" bags contain ")
        if rest == "no other bags.":
            yield outer, []
        else:
            yield outer, [parse_chunk(x) for x in rest.split(",")]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4
    """
    rules = dict(parse(text))
    inverse = defaultdict(set)
    for k, v in rules.items():
        for _, x in v:
            inverse[x].add(k)
    inverse = dict(inverse)
    seen = set()
    stack = ["shiny gold"]
    while stack:
        bag = stack.pop()
        seen.add(bag)
        for next_bag in inverse.get(bag, []):
            if next_bag in seen:
                continue
            stack.append(next_bag)
    return len(seen) - 1


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    32
    """
    rules = dict(parse(text))
    stack = [(1, 1, "shiny gold")]
    count = 0
    while stack:
        n, mult, bag = stack.pop()
        count += n * mult
        for next_n, next_bag in rules[bag]:
            next_mult = n * mult
            stack.append((next_n, next_mult, next_bag))
    return count - 1


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
