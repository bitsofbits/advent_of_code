from itertools import count


def parse_state(line):
    line = line.split(':')[1].strip()
    return {i for (i, x) in enumerate(line) if x == '#'}


def parse_rule(line):
    line = line.strip()
    v = line[-1] == '#'
    key_string = line.split('=>')[0].strip()
    key = 0
    for i, x in enumerate(key_string):
        if x == '#':
            key += 1 << i
    return key, v


def make_key(state, i):
    key = 0
    for k in range(5):
        if (i + k - 2) in state:
            key += 1 << k
    return key


def update(state, rules):
    candidates = set()
    for i in state:
        for di in (-2, -1, 0, 1, 2):
            candidates.add(i + di)

    next_state = set()
    for i in candidates:
        if make_key(state, i) in rules:
            next_state.add(i)

    return frozenset(next_state)


def parse(text):
    state, rules_string = text.strip().split('\n\n')
    state = parse_state(state)
    rules = set()
    for line in rules_string.strip().split('\n'):
        k, v = parse_rule(line)
        if v:
            rules.add(k)
    return frozenset(state), frozenset(rules)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    325
    """
    state, rules = parse(text)
    assert 0 not in rules
    for _ in range(20):
        state = update(state, rules)
    return sum(state)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    generations = 50_000_000_000
    state, rules = parse(text)
    for i in count():
        next_state = update(state, rules)
        if next_state == {x + 1 for x in state}:
            break
        state = next_state
    return sum(state) + len(state) * (generations - i)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
