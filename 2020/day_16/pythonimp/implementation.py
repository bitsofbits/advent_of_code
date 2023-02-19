def parse_rule(rule):
    name, ranges = rule.split(":")
    rng1, rng2 = [x.strip() for x in ranges.split("or")]
    rng1 = [int(x) for x in rng1.split("-")]
    rng2 = [int(x) for x in rng2.split("-")]
    return name, (rng1, rng2)


def parse(text):
    rules, my_tx, other_tx = text.strip().split("\n\n")
    rules = dict(parse_rule(x) for x in rules.split("\n"))
    my_tx = [int(x) for x in my_tx.split("\n")[1].split(",")]
    other_tx = [[int(x) for x in tx.split(",")] for tx in other_tx.split("\n")[1:]]
    return rules, my_tx, other_tx


def broken_rules(field, rules):
    broken = []
    for k, rule in rules.items():
        (lo1, hi1), (lo2, hi2) = rule
        if not (lo1 <= field <= hi1 or lo2 <= field <= hi2):
            broken.append(k)
    return broken


def errors(tx, rules):
    return {i: broken_rules(field, rules) for (i, field) in enumerate(tx)}


def is_invalid(tx, rules):
    return any((len(broken_rules(field, rules)) == len(rules)) for field in tx)


def error_sum(tx, rules):
    return sum(field * (len(broken_rules(field, rules)) == len(rules)) for field in tx)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    71
    """
    rules, my_tx, other_tx = parse(text)
    return sum(error_sum(tx, rules) for tx in other_tx)


EXAMPLE2_TEXT = """
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def find_field_mapping(rules, tickets):
    """
    >>> rules, my_tx, other_tx = parse(EXAMPLE2_TEXT)
    >>> find_field_mapping(rules, other_tx)
    {0: 'row', 1: 'class', 2: 'seat'}
    """
    tickets = [tx for tx in tickets if not is_invalid(tx, rules)]
    n_fields = max(len(x) for x in tickets)
    assert n_fields == len(rules)
    mapping = {i: set(rules) for i in range(n_fields)}
    for tx in tickets:
        for i, errs in errors(tx, rules).items():
            mapping[i] -= set(errs)

    keys = sorted(mapping, key=lambda i: len(mapping[i]))
    for i in keys:
        [rule] = mapping[i]
        for j in keys:
            if j != i and rule in mapping[j]:
                mapping[j].remove(rule)
    for i in keys:
        [mapping[i]] = mapping[i]

    return mapping


def part_2(text):
    rules, my_tx, other_tx = parse(text)
    field_mapping = find_field_mapping(rules, other_tx)
    prod = 1
    n_fields = 0
    for i, k in field_mapping.items():
        if k.startswith("departure"):
            prod *= my_tx[i]
            n_fields += 1
    assert n_fields == 6
    return prod


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
