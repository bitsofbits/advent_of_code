def parse_workflow(text):
    # bl{a<740:ls,gz}
    name, text = text.strip()[:-1].split('{')
    steps = []
    for chunk in text.split(','):
        if ':' in chunk:
            condition, target = chunk.split(':')
            field, op = condition[:2]
            value = condition[2:]
            condition = field, op, int(value)
        else:
            condition = None
            target = chunk
        steps.append((condition, target))
    return (name, steps)


def parse_item(text):
    item = {}
    for chunk in text[1:-1].strip().split(','):
        a, b = chunk.split('=')
        item[a] = int(b)
    return item


def parse(text):
    """
    >>> workflows, items = parse(EXAMPLE_TEXT)
    >>> workflows['in']
    [(('s', '<', 1351), 'px'), (None, 'qqz')]
    >>> items[0]
    {'x': 787, 'm': 2655, 'a': 1222, 's': 2876}
    """
    workflows, items = text.strip().split('\n\n')
    workflows = [parse_workflow(x) for x in workflows.strip().split('\n')]
    items = [parse_item(x) for x in items.strip().split('\n')]
    return dict(workflows), items


def process_part(part, workflows):
    key = 'in'
    while key not in 'AR':
        for condition, key in workflows[key]:
            if condition is None:
                break
            field, op, right = condition
            left = part[field]
            if op == '<':
                left, right = right, left
            if left > right:
                break
        else:
            return None
    return key


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    19114
    """
    workflows, parts = parse(text)
    accepted = []
    score = 0
    for part in parts:
        if process_part(part, workflows) == 'A':
            accepted.append(part)
            score += sum(part.values())
    return score


def process_interval(workflow, part):
    """
    >>> part = {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)}
    >>> workflows, items = parse(EXAMPLE_TEXT)
    >>> a, b = process_interval(workflows['in'], part)
    >>> a
    ('px', {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 1351)})
    >>> b
    ('qqz', {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1351, 4001)})
    """
    part = part.copy()
    for rule in workflow:
        condition, key = rule
        if condition is None:
            yield key, part
            continue
        field, op, threshold = condition
        lower, upper = part[field]
        if op == '<':
            if lower < threshold:
                new_part = part.copy()
                new_part[field] = lower, min(upper, threshold)
                yield key, new_part
            if upper <= threshold:
                return
            part[field] = (threshold, upper)
        if op == '>':
            if upper > threshold:
                new_part = part.copy()
                new_part[field] = max(lower, threshold + 1), upper
                yield key, new_part
            if lower >= threshold:
                return
            part[field] = (lower, threshold + 1)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    167409079868000
    """
    workflows, _ = parse(text)
    successful_ranges = []
    unclassified_parts = [
        ('in', {'x': (1, 4001), 'm': (1, 4001), 'a': (1, 4001), 's': (1, 4001)})
    ]
    while unclassified_parts:
        key, part = unclassified_parts.pop()
        for next_key, next_part in process_interval(workflows[key], part):
            if next_key == 'A':
                successful_ranges.append(next_part)
            elif next_key == 'R':
                continue
            else:
                unclassified_parts.append((next_key, next_part))

    count = 0
    for part in successful_ranges:
        n = 1
        for lower, upper in part.values():
            n *= upper - lower
        count += n
    return count


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
