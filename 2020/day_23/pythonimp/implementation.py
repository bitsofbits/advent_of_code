from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [3, 8, 9, 1, 2, 5, 4, 6, 7]
    """
    return [int(x) for x in text.strip()]


def apply_step(cups, max_label):
    """
    >>> cups = deque(parse(EXAMPLE_TEXT)); cups
    deque([3, 8, 9, 1, 2, 5, 4, 6, 7])
    >>> apply_step(cups, 9); cups
    deque([2, 8, 9, 1, 5, 4, 6, 7, 3])
    >>> apply_step(cups, 9); cups
    deque([5, 4, 6, 7, 8, 9, 1, 3, 2])
    """
    destination_label = cups[0] - 1
    if destination_label < 1:
        destination_label = max_label
    # Place the cups we want to remove at locations 0, 1, 2
    cups.rotate(-1)
    # Remove the first three cups
    removed = [cups.popleft() for _ in range(3)]

    while destination_label in removed:
        destination_label -= 1
        if destination_label < 1:
            destination_label = max_label

    # This is expensive <===
    cups.rotate(20000)
    destination_index = cups.index(destination_label, 0, 40000)
    cups.rotate(-20000)
    destination_index = (destination_index - 20000) % len(cups)

    # So is rotate if k is large
    # Insert removed at label
    cups.rotate(-(destination_index + 1))
    cups.extendleft(removed[::-1])
    cups.rotate(destination_index + 1)


def play_game_naive(cups, iterations):
    max_label = max(cups)
    cups = deque(cups)
    for _ in range(iterations):
        apply_step(cups, max_label=max_label)
    i = cups.index(1)
    return cups, i


def offset_mod(x, n):
    while x < 1:
        x += n
    while x > n:
        x -= n
    return x


def apply_step_ll(cups, origin, max_cup):
    target_label = offset_mod(origin - 1, max_cup)

    removed = []
    label = origin
    for _ in range(3):
        label = cups[label]
        removed.append(label)
    next_label = cups[label]

    while target_label in removed:
        target_label = offset_mod(target_label - 1, max_cup)

    # Cut out removed cups
    cups[origin] = next_label

    # Insert removed cups after target_label
    next_label = cups[target_label]
    last_label = target_label
    for label in removed:
        cups[last_label] = label
        last_label = label
    cups[last_label] = next_label
    cups[next_label] = cups[next_label]

    return cups, cups[origin]


def play_game_ll(cups, iterations):
    """
    >>> cups = deque(parse(EXAMPLE_TEXT)); cups
    deque([3, 8, 9, 1, 2, 5, 4, 6, 7])
    >>> cups, origin = play_game_ll(cups, 1)
    >>> origin
    2
    """
    raw_cups = cups
    n = len(cups)
    cups = [None] * (n + 1)
    for i, k in enumerate(raw_cups):
        cups[k] = raw_cups[(i + 1) % n]

    origin = raw_cups[0]
    for _ in range(iterations):
        cups, origin = apply_step_ll(cups, origin, n)

    return cups, origin


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    '67384529'
    """
    cups, origin = play_game_ll(parse(text), iterations=100)
    values = []
    n = cups[1]
    for _ in range(9):
        values.append(n)
        n = cups[n]
    values = deque(values)
    values.rotate(-values.index(1))
    return ''.join(str(x) for x in list(values)[1:])


def part_2(text, iterations=10000000):
    """
    >>> part_2(EXAMPLE_TEXT, 10000000)
    149245887792
    """
    initial_cups = parse(text)
    initial_cups.extend(range(max(initial_cups) + 1, 1000000 + 1))
    cups, origin = play_game_ll(initial_cups, iterations=iterations)
    a = cups[1]
    b = cups[a]
    return a * b


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
