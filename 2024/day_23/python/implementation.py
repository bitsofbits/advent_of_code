from itertools import combinations
from collections import defaultdict


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:4]
    [('kh', 'tc'), ('qp', 'kh'), ('de', 'cg'), ('ka', 'co')]
    """
    links = []
    for row in text.strip().split("\n"):
        a, b = row.split("-")
        links.append((a, b))
    return links


def find_linked(pairs):
    """
    >>> pairs = parse(EXAMPLE_TEXT)
    >>> for x in sorted(find_linked(pairs)): print(x)
    ('co', 'de', 'ta')
    ('co', 'ka', 'ta')
    ('de', 'ka', 'ta')
    ('qp', 'td', 'wh')
    ('tb', 'vc', 'wq')
    ('tc', 'td', 'wh')
    ('td', 'wh', 'yn')
    """
    ids = set()
    for pair in pairs:
        ids |= set(pair)
    ids = sorted(ids)
    links = set(tuple(sorted(x)) for x in pairs)

    ids_0 = [x for x in ids if x[0] < "t"]
    ids_t = [x for x in ids if x[0] == "t"]
    ids_1 = [x for x in ids if x[0] > "t"]

    # This is easy to brute force, but by breaking it up into cases, it runs much faster

    # 1 t value

    for i, a in enumerate(ids_0):
        for b in ids_0[i + 1 :]:
            for c in ids_t:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

    for a in ids_0:
        for b in ids_t:
            for c in ids_1:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

    for a in ids_t:
        for i, b in enumerate(ids_1):
            for c in ids_1[i + 1 :]:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

    # 2 t values

    for a in ids_0:
        for i, b in enumerate(ids_t):
            for c in ids_t[i + 1 :]:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

    for i, a in enumerate(ids_t):
        for b in ids_t[i + 1 :]:
            for c in ids_1:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

    # 3 t values

    for i, a in enumerate(ids_t):
        for dj, b in enumerate(ids_t[i + 1 :]):
            j = i + 1 + dj
            for c in ids_t[j + 1 :]:
                if ((a, b) in links) and ((a, c) in links) and ((b, c) in links):
                    yield (a, b, c)

def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7
    """
    pairs = parse(text)
    return sum(1 for _ in find_linked(pairs))


def are_fully_connected(computers, links):
    """ """
    computers = sorted(computers)
    for i, a in enumerate(computers):
        for b in computers[i + 1 :]:
            if (a, b) not in links:
                return False
    return True


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    'co,de,ka,ta'
    """
    pairs = parse(text)
    ids = set()
    for pair in pairs:
        ids |= set(pair)
    ids = sorted(ids)

    neighbors = defaultdict(set)
    for a, b in pairs:
        neighbors[a].add(b)
        neighbors[b].add(a)

    links = set(tuple(sorted(x)) for x in pairs)

    target = max(len(v) for v in neighbors.values()) + 1

    fully_connected = set()
    for target_size in reversed(range(target)):
        for a in ids:
            source_set = frozenset(neighbors[a] | {a})
            for target_set in combinations(source_set, target_size):
                if are_fully_connected(target_set, links):
                    fully_connected.add(frozenset(target_set))
        if fully_connected:
            break
    [result] = fully_connected
    return ",".join(sorted(result))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
