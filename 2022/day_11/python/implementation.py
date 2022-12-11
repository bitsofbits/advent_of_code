def dummy(path):
    """dummy func

    >>> 1 + 1
    3
    """
    pass


class Monkey:
    def __init__(
        self, operation, test, true_target, false_target, initial_items, divisor
    ):
        self.operation = operation
        self.test = test
        self.true_target = true_target
        self.false_target = false_target
        self.items = initial_items
        self.cumulative_inspections = 0
        self.divisor = divisor

    def take_turn(self):
        targets = {self.true_target: [], self.false_target: []}
        for x in self.items:
            self.cumulative_inspections += 1
            x = self.operation(x)
            x //= self.divisor
            if x % self.test == 0:
                targets[self.true_target].append(x)
            else:
                targets[self.false_target].append(x)
        self.items = []
        return targets


def make_op(txt):
    match txt.split():
        case ("old", "*", "old"):
            return lambda x: x * x
        case ("old", "*", arg):
            return lambda x, n=int(arg): x * n
        case ("old", "+", arg):
            return lambda x, n=int(arg): x + n
        case _:
            raise ValueError(txt)


def create_monkey(text, divisor):
    text = text.strip()
    lines = text.split("\n")
    assert len(lines) == 6
    ndx = int(lines[0][:-1].split()[-1])
    items = lines[1].split(":")[1].strip()
    items = [int(x.strip()) for x in items.split(",")]
    op = make_op(lines[2].split("=")[1].strip())
    test = int(lines[3].split()[-1])
    true_target = int(lines[4].split()[-1])
    false_target = int(lines[5].split()[-1])
    return ndx, Monkey(op, test, true_target, false_target, items, divisor)


def create_monkeys(text, divisor):
    return dict(create_monkey(x, divisor) for x in text.split("\n\n"))


def play_round(monkeys):
    modulo = 1
    for m in monkeys.values():
        modulo *= m.test
    for k in sorted(monkeys):
        targets = monkeys[k].take_turn()
        for kt, vt in targets.items():
            monkeys[kt].items.extend(vt)
    for m in monkeys.values():
        for i, v in enumerate(m.items):
            m.items[i] = v % modulo


def read_text(path):
    with open(path) as f:
        return f.read()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
