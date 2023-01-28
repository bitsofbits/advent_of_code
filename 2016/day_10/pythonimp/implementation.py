from collections import defaultdict


def parse(text):
    """
    >>> rules, startup = parse(EXAMPLE_TEXT)
    >>> for x in rules.items(): print(x)
    ('bot 2', ('bot 1', 'bot 0'))
    ('bot 1', ('output 1', 'bot 0'))
    ('bot 0', ('output 2', 'output 0'))
    >>> for x in sorted(startup): print(x)
    ('bot 1', 3)
    ('bot 2', 2)
    ('bot 2', 5)
    """
    startup = set()
    rules = {}
    for line in text.strip().split("\n"):
        match line.split():
            case "value", n, "goes", "to", "bot", bot:
                startup.add((f"bot {bot}", int(n)))
            case "bot", bot, "gives", "low", "to", k1, b1, "and", "high", "to", k2, b2:
                rules[f"bot {bot}"] = (f"{k1} {b1}", f"{k2} {b2}")
            case _:
                raise ValueError(line)
    return rules, startup


def process(text, for_part_1=False):
    rules, startup = parse(text)
    robots = defaultdict(list)
    for bot, value in startup:
        robots[bot].append(value)
    print(robots)
    while True:
        for bot, chips in robots.items():
            assert len(chips) <= 2
            if len(chips) == 2:
                low, high = sorted(chips)
                robots[bot] = []
                if for_part_1:
                    if (low, high) == (17, 61):
                        return bot
                bot_low, bot_high = rules[bot]
                robots[bot_low].append(low)
                robots[bot_high].append(high)
                break
        else:
            if for_part_1:
                raise RuntimeError("Doesn't terminate")
            else:
                return robots


def part_1(text):
    return process(text, for_part_1=True)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    robots = process(text, for_part_1=False)
    return robots["output 0"][0] * robots["output 1"][0] * robots["output 2"][0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
