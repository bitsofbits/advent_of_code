def parse_draw(text):
    text = text.strip()
    draw = {}
    for x in text.split(","):
        number_text, color = x.strip().split()
        draw[color] = int(number_text)
    return draw


def parse(text):
    """
    Lines look like:
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

    >>> for x in parse(EXAMPLE_TEXT):
    ...     print(x)
    (1, [{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}])
    (2, [{'blue': 1, 'green': 2}, {'green': 3, 'blue': 4, 'red': 1}, {'green': 1, 'blue': 1}])
    (3, [{'green': 8, 'blue': 6, 'red': 20}, {'blue': 5, 'red': 4, 'green': 13}, {'green': 5, 'red': 1}])
    (4, [{'green': 1, 'red': 3, 'blue': 6}, {'green': 3, 'red': 6}, {'green': 3, 'blue': 15, 'red': 14}])
    (5, [{'red': 6, 'blue': 1, 'green': 3}, {'blue': 2, 'red': 1, 'green': 2}])

    """
    for line in text.strip().split("\n"):
        name_text, game_text = line.split(":")
        _, number_text = name_text.split()
        game_number = int(number_text)
        game = [parse_draw(x.strip()) for x in game_text.split(";")]
        yield game_number, game


def is_possible(game, bag):
    for draw in game:
        for k, v in draw.items():
            if v > bag[k]:
                return False
    return True


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    8
    """
    bag = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for game_number, game in parse(text):
        if is_possible(game, bag):
            total += game_number
    return total


def min_bag(game):
    bag = {'red': 0, 'green': 0, 'blue': 0}
    for draw in game:
        for k, v in draw.items():
            bag[k] = max(bag[k], v)
    return bag


def bag_power(bag):
    return bag['red'] * bag['green'] * bag['blue']


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2286
    """
    total = 0
    for _, game in parse(text):
        total += bag_power(min_bag(game))
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
