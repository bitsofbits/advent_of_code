from collections import defaultdict
from functools import cmp_to_key


def parse(text):
    """
    >>> rules, updates = parse(EXAMPLE_TEXT)
    >>> rules
    {47: {29, 13, 61, 53}, 97: {75, 13, 47, 61, 53, 29}, 75: {13, 47, 29, 53, 61}, 61: {29, 53, 13}, 29: {13}, 53: {13, 29}}
    >>> updates[0]
    [75, 47, 61, 53, 29]
    """
    rule_text, print_text = text.strip().split('\n\n')
    rules = defaultdict(set)
    for line in rule_text.split('\n'):
        k, v = (int(x) for x in line.strip().split('|'))
        rules[k].add(v)
    updates = []
    for line in print_text.split('\n'):
        updates.append([int(x.strip()) for x in line.strip().split(',')])
    return dict(rules), updates


def is_ok(update, rules):
    for i, x in enumerate(update):
        for j in range(i + 1, len(update)):
            if update[j] not in rules.get(x, ()):
                return False
    return True  


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    143
    """
    rules, updates = parse(text)
    total = 0
    for x in updates:
        if is_ok(x, rules):
            total += x[len(x) // 2]
    return total


class Comp:
    def __init__(self, rules):
        self.rules = rules

    def __call__(self, x, y):
        if x == y:
            return 0
        return 1 if (y in self.rules.get(x, ())) else -1


def reorder(update, rules):
    return sorted(update, key=cmp_to_key(Comp(rules))) 


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    123
    """
    rules, updates = parse(text)
    total = 0
    for x in updates:
        if is_ok(x, rules):
            continue
        x = reorder(x, rules)
        total += x[len(x) // 2]
    return total

if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
