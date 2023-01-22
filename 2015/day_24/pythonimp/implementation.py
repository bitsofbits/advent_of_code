from math import inf


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    """
    return [int(x.strip()) for x in text.strip().split("\n")]


def min_qe(weights, target):
    weights = sorted(weights, reverse=True)
    pending = [(0, frozenset(), 0, 1)]
    min_length = inf
    min_qe = inf

    while pending:
        i0, used, wt, qe = pending.pop()
        for di, x in enumerate(weights[i0:]):
            if (next_wt := wt + x) <= target:
                i = i0 + di
                next_qe = qe * x
                next_used = used | {i}
                if next_wt == target:
                    if len(next_used) < min_length:
                        min_length = len(next_used)
                        min_qe = next_qe
                    else:
                        assert min_length == len(next_used)
                        min_qe = min(min_qe, next_qe)
                elif len(next_used) < min_length:
                    pending.append((i + 1, next_used, next_wt, next_qe))
    return min_qe


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    99
    """
    weights = parse(text)
    target = sum(weights) // 3
    assert 3 * target == sum(weights)
    # All possibilities for group1
    return min_qe(weights, target)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    44
    """
    weights = parse(text)
    target = sum(weights) // 4
    assert 4 * target == sum(weights)
    # All possibilities for group1
    return min_qe(weights, target)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
