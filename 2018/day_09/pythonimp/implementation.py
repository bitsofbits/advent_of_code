from collections import deque


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    (13, 799)
    """
    n_players, last_marble_score = tuple(int(x) for x in text.split())
    return n_players, last_marble_score


def play(n_players, last_marble_score):
    board = deque([0])
    players = deque([0] * n_players)
    for marble in range(1, last_marble_score + 1):
        if marble % 23 == 0:
            players[0] += marble
            board.rotate(7)
            players[0] += board.popleft()
        else:
            board.rotate(-2)
            board.appendleft(marble)
        players.rotate(-1)
    return players


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    32
    >>> part_1("10 1618")
    8317
    >>> part_1("13 7999")
    146373
    """
    n_players, last_marble_score = parse(text)
    players = play(n_players, last_marble_score)
    return max(players)


def part_2(text):
    n_players, last_marble_score = parse(text)
    players = play(n_players, 100 * last_marble_score)
    return max(players)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
