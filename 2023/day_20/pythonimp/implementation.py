from collections import deque
from itertools import count


def parse(text):
    """
    >>> list(parse(EXAMPLE_TEXT))[:2]
    [('broadcaster', 'B', ['a', 'b', 'c']), ('a', '%', ['b'])]
    """
    for line in text.strip().split('\n'):
        name, targets = line.split(' -> ')
        if name == 'broadcaster':
            kind = 'B'
        else:
            kind = name[0]
            name = name[1:]
        targets = targets.split(', ')
        yield (name, kind, targets)


class Broadcaster:
    """
    if inputs to all items is a vector I

    B I -> outputs


    """

    def __init__(self, name, inputs, outputs):
        assert not inputs
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def press_button(self):
        return {k: (self.name, False) for k in self.outputs}

    def process_signal(self, signal):
        high_times = {x + 1 for x in signal.high_times}
        low_times = {x + 1 for x in signal.low_times}
        new_signal = Signal(high_times=high_times, low_times=low_times)
        return {k: new_signal for k in self.outputs}


class FlipFlop:
    """
    S = S ^ (A &
    """

    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.state = False

    def process(self, source, value):
        if value:
            return {}
        else:
            self.state = not self.state
            return {k: (self.name, self.state) for k in self.outputs}

    # def process_signal(self, source, value):


class Signal:
    """
    >>> signal = Signal({0})

    >>> broadcaster = Broadcaster(name='B', inputs=[], outputs=['a', 'b'])
    >>> signal = broadcaster.process_signal(signal)
    >>> signal
    {'a': <.N..............................>, 'b': <.N..............................>}
    """

    repr_length = 32

    def __init__(self, low_times=(), high_times=()):
        self.low_times = set(low_times)
        self.high_times = set(high_times)

    def __repr__(self):
        chars = []
        for i in range(self.repr_length):
            if i in self.high_times:
                chars.append('P')
                assert i not in self.low_times
            elif i in self.low_times:
                chars.append('N')
            else:
                chars.append('.')
        return f"<{''.join(chars)}>"


class Conjunction:
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.state = {k: False for k in inputs}

    def process(self, source, value):
        self.state[source] = value
        if all(self.state.values()):
            return {k: (self.name, False) for k in self.outputs}
        else:
            return {k: (self.name, True) for k in self.outputs}


def build_network(items):
    items = list(items)
    network = {}
    # find inputs
    inputs_map = {'broadcaster': set()}
    for name, kind, outputs in items:
        for output_name in outputs:
            if output_name not in inputs_map:
                inputs_map[output_name] = set()
            inputs_map[output_name].add(name)

    for name, kind, outputs in items:
        inputs = inputs_map[name]
        if kind == 'B':
            network[name] = Broadcaster(name, inputs, outputs)
        elif kind == '%':
            network[name] = FlipFlop(name, inputs, outputs)
        elif kind == '&':
            network[name] = Conjunction(name, inputs, outputs)

    return network


def press_button(network):
    pulses = [1, 0]
    rx_low_count = 0
    queue = deque(list(network['broadcaster'].press_button().items()))
    while queue:
        target, (source, value) = queue.popleft()
        pulses[value] += 1
        if target == 'rx':
            rx_low_count += not value
        if target not in network:
            # print(name, "not in network")
            continue
        for new_target, new_value in network[target].process(source, value).items():
            queue.append((new_target, new_value))
    return pulses, rx_low_count


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    32000000

    >>> part_1(EXAMPLE2_TEXT)
    11687500
    """
    network = build_network(parse(text))
    low = high = 0
    for _ in range(1000):
        (L, H), _ = press_button(network)
        low += L
        high += H
    return low * high


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)

    vl -> 1
    cz -> 2
    dk -> 8
    cb -> 16 (odd)

    """
    network = build_network(parse(text))
    for k, v in network.items():
        print(k, len(v.inputs), v.__class__.__name__)
    # mr_state = network['zh'].state
    # last = mr_state.copy()
    # state_changes = {k: [] for k in mr_state.keys()}
    # for i in range(1, 100001):
    #     _, rx_low_count = press_button(network)
    #     for k, v in mr_state.items():
    #         if v != last[k]:
    #             state_changes[k].append((i, v))
    #     last = mr_state.copy()
    #     if rx_low_count == 1:
    #         print("WHOAH")
    #         break
    # assert len(state_changes) == len(mr_state)
    # cycle_info = {}
    # for k, v in state_changes.items():
    #     print(k)
    #     print([x[0] for x in v[-32:]])
    #     # assert len(v) >= 5
    #     # d1 = v[-3][0] - v[-5][0]
    #     # d2 = v[-1][0] - v[-3][0]
    #     # assert d1 == d2, (d1, d2, v[-3:])
    #     # i0 = v[-3][0] if v[-3][1] else v[-2][0]
    #     # cycle_info[k] = (i0, d1)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    doctest.testmod()
