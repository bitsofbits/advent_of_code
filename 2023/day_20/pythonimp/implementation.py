import math
from collections import deque


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


# def connected_to_rx(network):
#     """
#     everything is connected :-()
#     >>> connected_to_rx(parse(INPUT_TEXT))
#     """
#     network = list(network)
#     back_links = {'broadcaster': {}}
#     links = {}
#     for name, kind, targets in network:
#         for target in targets:
#             if target not in back_links:
#                 back_links[target] = set()
#             back_links[target].add(name)
#             if name not in links:
#                 links[name] = set()
#             links[name].add(target)

#     seen = set()
#     queue = ['vl']
#     while queue:
#         node = queue.pop()
#         if node in seen:
#             continue
#         seen.add(node)
#         for x in links[node]:
#             if x == 'zh':
#                 print(node)
#                 continue
#             # print(node)
#             queue.append(x)

#     print(len(seen), len(network))


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


def press_button(network, monitor='rx'):
    pulses = [1, 0]
    queue = deque(list(network['broadcaster'].press_button().items()))
    montored_values = {}
    while queue:
        target, (source, value) = queue.popleft()
        pulses[value] += 1
        if target == monitor:
            if source not in montored_values:
                montored_values[source] = [0, 0]
            montored_values[source][bool(value)] += 1

        if target not in network:
            continue
        for new_target, new_value in network[target].process(source, value).items():
            queue.append((new_target, new_value))
    return pulses, montored_values


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
    >>> part_2(INPUT_TEXT)

    vl -> 1
    cz -> 2
    dk -> 8
    cb -> 16 (odd

    243081086866484 is too high
    """
    network = build_network(parse(text))
    # for k, v in network.items():
    #     print(k, len(v.inputs), v.__class__.__name__)
    pulse_times = {
        'ks': [],
        'jt': [],
        'sx': [],
        'kb': [],
    }
    for i in range(1, 100001):
        _, values = press_button(network, monitor='zh')
        for k, v in values.items():
            if v[1] > 0:
                pulse_times[k].append(i)
    for k, v in pulse_times.items():
        print(k, v[:10])
    periods = [x[0] for x in pulse_times.values()]
    math.gcd(*periods) == 0
    return math.lcm(*periods)
    # assert len(state_changes) == len(mr_state)
    # cycle_info = {}
    # for k, v in state_changes.items():
    #     print(k)
    #     print([x[0] for x in v[-32:]])
    # assert len(v) >= 5
    # d1 = v[-3][0] - v[-5][0]
    # d2 = v[-1][0] - v[-3][0]
    # assert d1 == d2, (d1, d2, v[-3:])
    # i0 = v[-3][0] if v[-3][1] else v[-2][0]
    # cycle_info[k] = (i0, d1)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()
    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()
    doctest.testmod()
