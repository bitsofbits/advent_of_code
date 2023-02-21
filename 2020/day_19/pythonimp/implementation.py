from functools import cache


def parse_sub_rule(text):
    text = text.strip()
    return tuple(int(x) for x in text.split())


def parse_rule(text):
    name, rule = text.split(": ")
    if rule.startswith('"'):
        assert rule.endswith('"')
        rule = (rule[1:-1],)
    else:
        rule = [parse_sub_rule(x) for x in rule.split("|")]
    return int(name), rule


def parse(text):
    rules, messages = text.strip().split("\n\n")
    return dict(parse_rule(x) for x in rules.split("\n")), messages.split("\n")


# def matches(tokens, rules):
#     stack = [tokens]
#     seen = set()
#     while stack:
#         tokens = stack.pop()
#         if tokens in seen:
#             continue
#         seen.add(tokens)
#         if tokens == (0,):
#             return True
#         m = len(tokens) + 1
#         for k, v in rules.items():
#             for r in v:
#                 n = len(r)
#                 for i in range(m - n):
#                     if r == tokens[i : i + n]:
#                         stack.append(tokens[:i] + (k,) + tokens[i + n :])
#     return False


# def matches2(tokens, rules, cache):
#     if tokens in cache:
#         return cache[tokens]
#     if tokens == (0,):
#         return True
#     m = len(tokens) + 1
#     for k, v in rules.items():
#         for r in v:
#             n = len(r)
#             for i in range(m - n):
#                 if r == tokens[i : i + n]:
#                     if matches2(tokens[:i] + (k,) + tokens[i + n :], rules, cache):
#                         cache[tokens] = True
#                         return True
#     cache[tokens] = False
#     return False


@cache
def partition(tokens, n):
    m = len(tokens)
    match n:
        case 1:
            return [(tokens,)]
        case 2:
            return [(tokens[:i], tokens[i:]) for i in range(1, m)]
        case 3:
            return [
                (tokens[:i], tokens[i:j], tokens[j:])
                for i in range(1, m - 1)
                for j in range(i + 1, m)
            ]
        case _:
            raise ValueError(n)


def match(tokens, rules, target):
    @cache
    def _match(tkns, tgt):
        for r in rules[tgt]:
            n = len(tkns)
            match r:
                case (r0,):
                    if _match(tkns, r0):
                        return True
                case (r0, r1):
                    for i in range(1, n):
                        if _match(tkns[:i], r0) and _match(tkns[i:], r1):
                            return True
                case (r0, r1, r2):
                    for i in range(1, n - 1):
                        for j in range(i + 1, n):
                            if (
                                _match(tkns[:i], r0)
                                and _match(tkns[i:j], r1)
                                and _match(tkns[j:], r2)
                            ):
                                return True
                case r if isinstance(r, str):
                    if (r,) == tkns:
                        return True
                case _:
                    raise ValueError(r)
        return False

    return _match(tokens, target)


def part_1(text):
    """m
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    rules, messages = parse(text)
    return sum(match(tuple(msg), rules, 0) for msg in messages)


EXTRA_RULES = """
8: 42 | 42 8
11: 42 31 | 42 11 31
"""


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    new_rules = dict(parse_rule(x) for x in EXTRA_RULES.strip().split("\n"))
    rules, messages = parse(text)
    rules.update(new_rules)
    return sum(match(tuple(msg), rules, 0) for msg in messages)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
