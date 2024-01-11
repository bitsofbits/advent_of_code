from collections import defaultdict
from itertools import count


def parse(text):
    """
    >>> parents, children = parse(EXAMPLE_TEXT)
    """
    children = defaultdict(set)
    parents = {}
    for line in text.strip().split('\n'):
        parent, child = line.split(')')
        children[parent].add(child)
        assert child not in parents
        parents[child] = parent
    return parents, dict(children)


def orbits_for(x, parents):
    """
    >>> parents, children = parse(EXAMPLE_TEXT)
    >>> orbits_for('COM', parents)
    0
    >>> orbits_for('L', parents)
    7
    >>> orbits_for('D', parents)
    3
    """
    for i in count(0):
        if x == 'COM':
            return i
        x = parents[x]


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    42
    """
    parents, children = parse(text)
    return sum(orbits_for(x, parents) for x in parents)


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    4
    """
    parents, children = parse(text)
    my_path_to_com = []
    x = 'YOU'
    while x != 'COM':
        x = parents[x]
        my_path_to_com.append(x)

    objects_on_my_path = set(my_path_to_com)
    santas_path_to_me = []
    x = 'SAN'
    while x not in objects_on_my_path:
        x = parents[x]
        santas_path_to_me.append(x)

    my_path_to_santa = []
    for x in my_path_to_com:
        my_path_to_santa.append(x)
        if x == santas_path_to_me[-1]:
            break

    return len(my_path_to_santa[1:]) + len(santas_path_to_me[1:])


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example2.txt") as f:
        EXAMPLE2_TEXT = f.read()

    doctest.testmod()
