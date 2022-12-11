"""Compute how much Monkey business some monkeys get up to

>>> path = "data/example.txt"
>>> print(compute_business(load_monkeys(path, 3), 20))
10605
>>> print(compute_business(load_monkeys(path, 1), 10000))
2713310158
"""


def extract_from(line, prefix, factory, suffix=""):
    line = line.strip()
    n = len(prefix)
    assert line[:n] == prefix
    line = line[n:]
    n = len(suffix)
    if n > 0:
        assert line[-n:] == suffix
        line = line[:-n]
    return factory(line.strip())


def make_op(text):
    match text.split():
        case ("old", "*", "old"):
            return lambda x: x * x
        case ("old", "*", arg):
            return lambda x, n=int(arg): x * n
        case ("old", "+", arg):
            return lambda x, n=int(arg): x + n
        case _:
            raise ValueError(text)


def make_items(text):
    return lambda x: [int(v.strip()) for v in x.split(",")]


class Monkey:
    """A monkey who does monkey stuff

    Args:
        identifier: some way to identify the monkey, in this case it's numbers
        operation: how to modify worry level when this monkey has your stuff
        test_value: monkey to toss stuff to is based on `worry % test_value == 0`
        true_target: monkey with this identifier gets an item when test is true
        false_target: otherwise this monkey gets it
        initial items: worry levels for items the monkey starts with
        relief_factor: worry is reduced by this factor each round
    """

    def __init__(
        self,
        identifier,
        operation,
        test_value,
        true_target,
        false_target,
        initial_items,
        relief_factor,
    ):
        self.identifier = identifier
        self.operation = operation
        self.test_value = test_value
        self.true_target = true_target
        self.false_target = false_target
        self.items = initial_items
        self.relief_factor = relief_factor
        self.inspections = 0

    def take_turn(self):
        targets = {self.true_target: [], self.false_target: []}
        for x in self.items:
            self.inspections += 1
            x = self.operation(x)
            x //= self.relief_factor
            if x % self.test_value == 0:
                targets[self.true_target].append(x)
            else:
                targets[self.false_target].append(x)
        self.items = []
        return targets

    @staticmethod
    def play_round(monkeys):
        modulo = 1
        for m in monkeys.values():
            modulo *= m.test_value
        for k in sorted(monkeys):
            targets = monkeys[k].take_turn()
            for kt, vt in targets.items():
                monkeys[kt].items.extend(vt)
        for m in monkeys.values():
            for i, v in enumerate(m.items):
                m.items[i] = v % modulo

    @staticmethod
    def compute_business(monkeys, rounds):
        for _ in range(rounds):
            Monkey.play_round(monkeys)
        ordered = sorted(monkeys, key=lambda k: monkeys[k].inspections)
        return monkeys[ordered[-1]].inspections * monkeys[ordered[-2]].inspections

    @classmethod
    def from_text(cls, text, relief_factor):
        """Create a monkey from a text description

        Format looks like this:

            Monkey 0:
              Starting items: 79, 98
              Operation: new = old * 19
              Test: divisible by 23
                If true: throw to monkey 2
                If false: throw to monkey 3
        """
        text = text.strip()
        lines = text.split("\n")
        assert len(lines) == 6
        identifier = extract_from(lines[0], prefix="Monkey", suffix=":", factory=int)
        items = extract_from(lines[1], prefix="Starting items:", factory=make_items)
        op = extract_from(lines[2], prefix="Operation: new =", factory=make_op)
        test_value = extract_from(lines[3], "Test: divisible by", factory=int)
        true_target = extract_from(lines[4], "If true: throw to monkey", factory=int)
        false_target = extract_from(lines[5], "If false: throw to monkey", factory=int)
        return cls(
            identifier, op, test_value, true_target, false_target, items, relief_factor
        )


def compute_business(monkeys, rounds):
    for _ in range(rounds):
        Monkey.play_round(monkeys)
    ordered = sorted(monkeys, key=lambda k: monkeys[k].inspections)
    return monkeys[ordered[-1]].inspections * monkeys[ordered[-2]].inspections


def load_monkeys(path, relief_factor):
    with open(path) as f:
        text = f.read()
    monkey_list = [Monkey.from_text(x, relief_factor) for x in text.split("\n\n")]
    return {x.identifier: x for x in monkey_list}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
