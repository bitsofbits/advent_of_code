from collections import deque


def parse_deck(text):
    assert text.startswith("Player")
    return deque([int(x.strip()) for x in text.split("\n")[1:] if x.strip()])


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    (deque([9, 2, 6, 3, 1]), deque([5, 8, 4, 7, 10]))
    """
    deck1, deck2 = text.strip().split("\n\n")
    return parse_deck(deck1), parse_deck(deck2)


def play(deck1, deck2):
    while deck1 and deck2:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)


def score(deck):
    deck = deck.copy()
    scale = 1
    score = 0
    while deck:
        score += scale * deck.pop()
        scale += 1
    return score


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    306
    """
    deck1, deck2 = parse(text)
    play(deck1, deck2)
    return score(deck1) + score(deck2)


def recursive_play(deck1, deck2):
    seen = set()
    while deck1 and deck2:
        key = (tuple(deck1), tuple(deck2))
        if key in seen:
            return True
        seen.add(key)
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > len(deck1) or card2 > len(deck2):
            # One of card values is too high to play recursively
            player_1_wins = card1 > card2
        else:
            subdeck1 = deque(list(deck1)[:card1])
            subdeck2 = deque(list(deck2)[:card2])
            player_1_wins = recursive_play(subdeck1, subdeck2)
        if player_1_wins:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    assert len(deck1) == 0 or len(deck2) == 0
    player_1_wins = len(deck1) > 0
    return player_1_wins


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    291
    """
    deck1, deck2 = parse(text)
    recursive_play(deck1, deck2)
    return score(deck1) + score(deck2)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
