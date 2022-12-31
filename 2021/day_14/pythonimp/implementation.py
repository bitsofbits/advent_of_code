from collections import Counter, defaultdict
from functools import cache

EXAMPLE_TEXT = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def parse(text):
    """
    >>> template, rules = parse(EXAMPLE_TEXT)
    >>> template
    'NNCB'
    >>> sorted(rules.items())[:4]
    [('BB', 'N'), ('BC', 'B'), ('BH', 'H'), ('BN', 'B')]
    """
    template, rules = text.strip().split("\n\n")
    template = template.strip()
    rules = dict(x.strip().split(" -> ") for x in rules.split("\n"))
    return template, rules


def polymerize(template, rules, steps):
    """
    >>> template, rules = parse(EXAMPLE_TEXT)
    >>> polymerize(template, rules, 4)
    'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB'
    """

    @cache
    def step(unit):
        """Perform one polymerization step"""
        n = len(unit)
        if n < 2:
            return rules.get(unit, unit)
        start = step(unit[: n // 2])
        mid = rules.get((unit[n // 2 - 1 : n // 2 + 1]), "")
        end = step(unit[n // 2 :])
        return start + mid + end

    polymer = template
    for _ in range(steps):
        polymer = step(polymer)
    return polymer


def score(polymer):
    counter = Counter(polymer)
    (_, most), *_, (_, least) = counter.most_common()
    return most - least


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1588
    """
    template, rules = parse(text)
    polymer = polymerize(template, rules, 10)
    return score(polymer)


def unordered_insert(pairs, expansions):
    new_pairs = defaultdict(int)
    for p in pairs:
        for x in expansions[p]:
            new_pairs[x] += pairs[p]
    return new_pairs


def unordered_polymerize(template, rules, steps):
    pairs = defaultdict(int)
    for i in range(len(template) - 1):
        p = template[i : i + 2]
        pairs[p] += 1

    expansions = {k: (k[0] + v, v + k[1]) for (k, v) in rules.items()}

    for _ in range(steps):
        pairs = unordered_insert(pairs, expansions)
    return pairs


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2188189693529
    """
    template, rules = parse(text)
    pairs = unordered_polymerize(template, rules, 40)
    raw_counts = defaultdict(int)
    for k, v in pairs.items():
        for x in k:
            raw_counts[x] += v
    # Every pair is counted twice except the two end points so add them in
    raw_counts[template[0]] += 1
    raw_counts[template[-1]] += 1
    for x in raw_counts.values():
        assert x % 2 == 0
    counts = {k: v // 2 for (k, v) in raw_counts.items()}
    return max(counts.values()) - min(counts.values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
