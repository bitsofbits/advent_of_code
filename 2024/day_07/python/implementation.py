from math import log10

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:3]
    [(190, (10, 19)), (3267, (81, 40, 27)), (83, (17, 5))]
    """
    equations = []
    for line in text.strip().split('\n'):
        answer_text, values_text = line.split(':')
        answer = int(answer_text.strip())
        values = tuple(int(x) for x in values_text.strip().split())
        equations.append((answer, values))
    return equations


def has_zero_values(equations):
    for _, values in equations:
        if 0 in values:
            return True
    return False

def possible_answers(values, max_value):
    if len(values) == 1:
        return set(values)
    initial = possible_answers(values[:-1], max_value)
    result = set()
    v1 = values[-1]
    for x in initial:
        y = v1 + x
        if y <= max_value:
            result.add(y)
        y = v1 * x
        if y <= max_value:
            result.add(y)
    return result


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3749
    """
    equations = parse(text)
    assert not has_zero_values(equations)
    total = 0
    for answer, values in equations:
        possible = possible_answers(values, answer)
        if answer in possible:
            total += answer
    return total

def possible_answers_2(values, max_value):
    if len(values) == 1:
        return set(values)
    initial = possible_answers_2(values[:-1], max_value)
    result = set()
    v1 = values[-1]
    for x in initial:
        y = v1 + x
        if y <= max_value:
            result.add(y)
        y = v1 * x
        if y <= max_value:
            result.add(y)
        digits = int(log10(v1)) + 1
        y = x * 10 ** digits + v1
        if y <= max_value:
            result.add(y)
    return result


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    11387
    """
    equations = parse(text)
    assert not has_zero_values(equations)
    total = 0
    for answer, values in equations:
        possible = possible_answers_2(values, answer)
        if answer in possible:
            total += answer
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
