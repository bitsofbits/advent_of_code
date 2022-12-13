from ast import literal_eval


class Packet:
    """
    >>> pairs = load_packets_pairs("data/example.txt")
    >>> [a < b for (a, b) in pairs]
    [True, True, False, True, False, True, False, False]
    """

    def __init__(self, text):
        self.data = literal_eval(text)

    @classmethod
    def _lt(cls, self_data, other_data):
        match self_data, other_data:
            case int(x), int(y):
                return (x < y) - (x > y)
            case list(x), int(y):
                return cls._lt(x, [y])
            case int(x), list(y):
                return cls._lt([x], y)
            case list(x), list(y):
                for a, b in zip(x, y):
                    lt = cls._lt(a, b)
                    if lt != 0:
                        return lt
                return cls._lt(len(x), len(y))
            case _:
                raise ValueError(f"unhandled case {self_data}, {other_data}")

    def __lt__(self, other):
        return self._lt(self.data, other.data) == 1

    def __str__(self):
        return f"{self.data}".replace(" ", "")

    def __repr__(self):
        return f"Packet('{self.data}')"


def load_packets_pairs(path):
    """

    >>> pairs = load_packets_pairs("data/example.txt")
    >>> len(pairs)
    8
    >>> pairs[0]
    (Packet('[1, 1, 3, 1, 1]'), Packet('[1, 1, 5, 1, 1]'))
    """
    with open(path) as f:
        text = f.read().strip()
        pairs = [x.split("\n") for x in text.split("\n\n")]
        for i, p in enumerate(pairs):
            assert len(p) == 2
            pairs[i] = (Packet(p[0]), Packet(p[1]))
    return pairs


def _sort_packets(pairs):
    """
    >>> pairs = load_packets_pairs("data/example.txt")
    >>> for x in _sort_packets(pairs)[0]: print(x)
    []
    [[]]
    [[[]]]
    [1,1,3,1,1]
    [1,1,5,1,1]
    [[1],[2,3,4]]
    [1,[2,[3,[4,[5,6,0]]]],8,9]
    [1,[2,[3,[4,[5,6,7]]]],8,9]
    [[1],4]
    [[2]]
    [3]
    [[4,4],4,4]
    [[4,4],4,4,4]
    [[6]]
    [7,7,7]
    [7,7,7,7]
    [[8,7,6]]
    [9]
    """
    dividers = [Packet(x) for x in ("[[2]]", "[[6]]")]
    packets = sum((list(x) for x in pairs), []) + dividers
    packets.sort()
    return packets, dividers


def find_decoder_key(pairs):
    """
    >>> pairs = load_packets_pairs("data/example.txt")
    >>> find_decoder_key(pairs)
    140
    """
    packets, dividers = _sort_packets(pairs)
    indices = []
    for i, p in enumerate(packets):
        if p in dividers:
            indices.append(i + 1)
    (a, b) = indices
    return a * b


if __name__ == "__main__":
    import doctest

    doctest.testmod()
