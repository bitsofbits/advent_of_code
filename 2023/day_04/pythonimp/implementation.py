def parse_card(line):
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    name, rest = line.split(':')
    winners_text, numbers_text = rest.split('|')
    winners = set(int(x) for x in winners_text.strip().split())
    numbers = [int(x) for x in numbers_text.strip().split()]
    return name, winners, numbers


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[0]
    ('Card 1', {41, 48, 17, 83, 86}, [83, 86, 6, 31, 17, 9, 48, 53])
    """
    for line in text.strip().split('\n'):
        yield parse_card(line)


def compute_score(winners, numbers):
    n_matches = sum(1 for x in numbers if x in winners)
    return 0 if (n_matches == 0) else 2 ** (n_matches - 1)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    13
    """
    return sum(compute_score(winners, numbers) for (_, winners, numbers) in parse(text))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    30
    """
    scratch_cards = list(parse(text))
    card_counts = {name: 1 for (name, _, _) in scratch_cards}
    card_contents = {
        name: (winners, numbers) for (name, winners, numbers) in parse(text)
    }
    card_names = sorted(name for (name, _, _) in scratch_cards)
    for i, name in enumerate(card_names):
        winners, numbers = card_contents[name]
        n_matches = sum(1 for x in numbers if x in winners)
        for new_name in card_names[i + 1 : i + 1 + n_matches]:
            card_counts[new_name] += card_counts[name]
    return sum(card_counts.values())


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
