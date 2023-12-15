def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ['rn=1', 'cm-', 'qp=3', 'cm=2', 'qp-', 'pc=4', 'ot=9', 'ab=5', 'pc-', 'pc=6', 'ot=7']
    """
    return text.strip().split(',')


def compute_hash(text):
    """
    >>> for x in parse(EXAMPLE_TEXT):
    ...     print(compute_hash(x))
    30
    253
    97
    47
    14
    180
    9
    197
    48
    214
    231
    """
    hash = 0
    for x in text:
        hash += ord(x)
        hash *= 17
        hash %= 256
    return hash


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1320
    """
    return sum(compute_hash(x) for x in parse(text))


def compute_focusing_power(box_number, box):
    return (box_number + 1) * sum((i + 1) * x for (i, (_, x)) in enumerate(box))


def update_boxes(boxes, command):
    """
    >>> boxes = [[] for i in range(256)]
    >>> for x in parse(EXAMPLE_TEXT):
    ...     update_boxes(boxes, x)
    >>> print(boxes[:4])
    [[('rn', 1), ('cm', 2)], [], [], [('ot', 7), ('ab', 5), ('pc', 6)]]
    """
    if command.endswith('-'):
        label = command[:-1]
        index = compute_hash(label)
        box = boxes[index]
        for i, (L, _) in enumerate(box):
            if L == label:
                box.pop(i)
                break
    else:
        label, power_str = command.split('=')
        power = int(power_str)
        index = compute_hash(label)
        box = boxes[index]
        for i, (L, _) in enumerate(box):
            if L == label:
                box[i] = (label, power)
                break
        else:
            box.append((label, power))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    145
    """
    total = 0
    boxes = [[] for i in range(256)]
    for x in parse(text):
        update_boxes(boxes, x)
    for i, box in enumerate(boxes):
        total += compute_focusing_power(i, box)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
