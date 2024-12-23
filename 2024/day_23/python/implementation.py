from dataclasses import dataclass
from itertools import combinations

def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:4]
    [('kh', 'tc'), ('qp', 'kh'), ('de', 'cg'), ('ka', 'co')]
    """
    links = []
    for row in text.strip().split('\n'):
        a, b = row.split('-')
        links.append((a, b))
    return links

@dataclass
class Element:
    node_id : str
    parent : str
    size: int


def add_node_to(forest, node_id):
    if node_id not in forest:
        forest[node_id] = Element(node_id=node_id, parent=None, size=1)

def is_root(element):
    return element.parent == None

def find_root(element):
    if element.parent is None:
        return element
    else:
        element.parent = find_root(element.parent)
        return element if (element.parent is None) else element.parent

def merge_sets_containing(element_a, element_b):
    root_a = find_root(element_a)
    root_b = find_root(element_b)

    if root_a == root_b:
        return

    if root_a.size < root_b.size:
        (root_a, root_b) = (root_b, root_a)

    root_b.parent = root_a
    root_a.size += root_b.size

def has_t(combination):
    for x in combination:
        if 't' in x:
            return True
    return False

def linked(triple, links):
    a, b, c = triple
    return (a, b) in links and (a, c) in links and (b, c) in links

def find_linked(pairs):
    """
    >>> pairs = parse(EXAMPLE_TEXT)
    >>> for x in find_linked(pairs): print(x)
    ('co', 'de', 'ta')
    ('co', 'ka', 'ta')
    ('de', 'ka', 'ta')
    ('qp', 'td', 'wh')
    ('tb', 'vc', 'wq')
    ('tc', 'td', 'wh')
    ('td', 'wh', 'yn')

    2819 too high
    """
    ids = set()
    for pair in pairs:
        ids |= set(pair)
    ids = sorted(ids)
    links = set(tuple(sorted(x)) for x in pairs)

    for triple in combinations(ids, 3):
        if has_t(triple) and linked(triple, links):
            yield triple


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    7

    2819 too high
    """
    pairs = parse(text)
    return sum(1 for _ in find_linked(pairs))

def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
