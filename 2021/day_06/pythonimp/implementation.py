EXAMPLE_TEXT = """
3,4,3,1,2
"""


class Fish:
    def __init__(self, n, count=1):
        self.n = n
        self.count = count

    def __str__(self):
        if self.count == 1:
            return str(self.n)
        else:
            return f"{self.n} x {self.count}"

    def update(self):
        self.n -= 1
        if self.n < 0:
            self.n = 6
            return [Fish(8, self.count)]
        return []

    __repr__ = __str__


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [3, 4, 3, 1, 2]
    """
    return [Fish(int(x)) for x in text.strip().split(",")]


def simulate(fish, days):
    compact_fish = {i: Fish(i, count=0) for i in range(9)}
    for f in fish:
        compact_fish[f.n].count += 1
    for _ in range(days):
        new_fish = {i: Fish(i, count=0) for i in range(9)}
        for f in compact_fish.values():
            for new_f in f.update():
                new_fish[new_f.n].count += new_f.count
            new_fish[f.n].count += f.count
        compact_fish = new_fish
    return sum(f.count for f in compact_fish.values())


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5934
    """
    fish = parse(text)
    return simulate(fish, 80)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    26984457539
    """
    fish = parse(text)
    return simulate(fish, 256)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
