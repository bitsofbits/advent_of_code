from collections import Counter, defaultdict


class DeterministicGame:
    def __init__(self, pos1, pos2):
        self.pos = {1: pos1, 2: pos2}
        self.t = 0
        self.score = {1: 0, 2: 0}

    def advance(self, player):
        total = 0
        for _ in range(3):
            n = self.t % 100 + 1
            self.t += 1
            total += n
        self.pos[player] = (self.pos[player] + total - 1) % 10 + 1
        self.score[player] += self.pos[player]
        if self.score[player] >= 1000:
            raise StopIteration()

    def play(self):
        try:
            while True:
                self.advance(1)
                self.advance(2)
        except StopIteration:
            pass

    def __repr__(self):
        return (
            f"DeterministicGame({self.score[1]}@{self.pos[1]}, "
            f"{self.score[2]}@{self.pos[2]}, t={self.t})"
        )

    __str__ = __repr__


class QuantumGame:
    def __init__(self, pos1, pos2):
        self.states = {((pos1, pos2), (0, 0)): 1}
        self.wins = {0: 0, 1: 0}

        moves = [0]
        for _ in range(3):
            new_moves = []
            for roll in [1, 2, 3]:
                for x in moves:
                    new_moves.append(x + roll)
            moves = new_moves
        self.moves = dict(Counter(moves))

    def advance(self, i):
        new = defaultdict(int)
        for mv, cnt1 in self.moves.items():
            for (pos, scr), cnt2 in self.states.items():
                cnt = cnt1 * cnt2
                pos = list(pos)
                scr = list(scr)
                pos[i] = (pos[i] + mv - 1) % 10 + 1
                scr[i] += pos[i]
                if scr[i] >= 21:
                    self.wins[i] += cnt
                else:
                    new[(tuple(pos), tuple(scr))] += cnt
        self.states = dict(new)

    def play(self):
        while self.states:
            self.advance(0)
            self.advance(1)

    def __repr__(self):
        return "QuantumGame(...)"

    __str__ = __repr__


def parse_1(text):
    """
    >>> parse_1(EXAMPLE_TEXT)
    DeterministicGame(0@4, 0@8, t=0)
    """
    l1, l2 = text.strip().split("\n")
    p1 = int(l1.split()[-1])
    p2 = int(l2.split()[-1])
    return DeterministicGame(p1, p2)


def parse_2(text):
    """
    >>> parse_2(EXAMPLE_TEXT)
    QuantumGame(...)
    """
    l1, l2 = text.strip().split("\n")
    p1 = int(l1.split()[-1])
    p2 = int(l2.split()[-1])
    return QuantumGame(p1, p2)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    739785
    """
    game = parse_1(text)
    game.play()
    return game.t * min(game.score.values())


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    444356092776315
    """
    game = parse_2(text)
    game.play()
    return max(game.wins.values())


if __name__ == "__main__":
    import doctest

    with open("../data/example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
