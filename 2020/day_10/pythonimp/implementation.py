from collections import defaultdict, deque


def parse(text):
    return [int(x) for x in text.strip().split()]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    220
    """
    stack = sorted(parse(text))
    stack.append(stack[-1] + 3)
    x0 = 0
    j1 = j3 = 0
    for x1 in stack:
        delta = x1 - x0
        assert 1 <= delta <= 3
        if delta == 1:
            j1 += 1
        if delta == 3:
            j3 += 1
        x0 = x1
    return j1 * j3


# def count_arangements(adapters):
#     adapters = sorted(adapters)
#     queue = deque([(0, 0, 1)])
#     final = adapters[-1]
#     count = 0
#     states = {}
#     while queue:
#         val, ndx, cnt = queue.popleft()
#         if val == final:
#             count
#         for i, next_val in enumerate(adapters[ndx:]):
#             if next_val < val + 1:
#                 continue
#             if next_val > val + 3:
#                 break
#             next_ndx = ndx + i + 1
#             next_used = used.copy()
#             next_used.append(next_val)
#             queue.append((next_val, next_ndx, next_used))

# def count_arangements(adapters)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    19208
    """
    adapters = parse(text)
    adapters.extend([0])
    adapters.sort(reverse=True)
    N = len(adapters)
    counts = {max(adapters) + 3: 1}
    for x in adapters:
        counts[x] = sum(counts.get(x + i, 0) for i in [1, 2, 3])
    return counts[0]


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
