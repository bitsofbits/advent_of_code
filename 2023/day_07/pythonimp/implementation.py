from collections import Counter


def compute_kind(hand):
    counts = Counter(hand).most_common()
    _, top_count = counts[0]
    if top_count == 5:
        return 6
    if top_count == 4:
        return 5
    _, second_count = counts[1]
    if top_count == 3:
        if second_count == 2:
            return 4
        else:
            return 3
    if top_count == 2:
        if second_count == 2:
            return 2
        else:
            return 1
    return 0


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [['32T3K', '765'], ['T55J5', '684']]
    """
    for line in text.strip().split("\n"):
        yield line.strip().split()


def numerize(hand):
    return ["23456789TJQKA".index(x) for x in hand]


def order_hands(hands):
    hands = [(compute_kind(hand), numerize(hand), bid) for (hand, bid) in hands]
    hands.sort()
    return [(hand, bid) for (_, hand, bid) in hands]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    6440
    """
    hands = list(parse(text))
    hands = order_hands(hands)
    total_winnings = 0
    for i, (hand, bid) in enumerate(hands):
        total_winnings += int(bid) * (i + 1)
    return total_winnings


def numerize_2(hand):
    return ["J23456789TQKA".index(x) for x in hand]


def compute_kind_with_jokers(hand):
    normal_cards = [x for x in hand if x != 'J']
    n_jokers = len(hand) - len(normal_cards)
    if n_jokers == len(hand):
        return 6
    counts = Counter(normal_cards).most_common()
    _, top_count = counts[0]
    top_count += n_jokers
    if top_count == 5:
        return 6
    if top_count == 4:
        return 5
    _, second_count = counts[1]
    if top_count == 3:
        if second_count == 2:
            return 4
        else:
            return 3
    if top_count == 2:
        if second_count == 2:
            return 2
        else:
            return 1
    return 0


def order_hands_with_jokers(hands):
    hands = [
        (compute_kind_with_jokers(hand), numerize_2(hand), bid) for (hand, bid) in hands
    ]
    hands.sort()
    return [(hand, bid) for (_, hand, bid) in hands]


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    5905

    253313241 is too low
    """
    hands = list(parse(text))
    hands = order_hands_with_jokers(hands)
    total_winnings = 0
    for i, (hand, bid) in enumerate(hands):
        total_winnings += int(bid) * (i + 1)
    return total_winnings


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
