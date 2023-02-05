from collections import defaultdict


def parse(text):
    tower = {}
    for line in text.strip().split("\n"):
        line = line.strip()
        if "->" in line:
            disk, children = line.split("->")
            children = frozenset(x.strip() for x in children.split(","))
        else:
            disk = line
            children = frozenset()
        disk = disk.strip()
        name, weight = disk.split()
        weight = int(weight[1:-1])
        tower[name] = (weight, children)
    return tower


def find_root(tower):
    parents = {}
    for name, (_, children) in tower.items():
        for child in children:
            assert child not in parents
            parents[child] = name
    # Pick any child
    for child in children:
        break
    while child in parents:
        child = parents[child]
    return child


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    'tknk'
    """
    return find_root(parse(text))

    # parents = {}
    # for name, _, children in parse(text):
    #     for child in children:
    #         assert child not in parents
    #         parents[child] = name
    # # Pick any child
    # for child in children:
    #     break
    # while child in parents:
    #     child = parents[child]
    # return child


def weight_of(name, tower):
    wt, children = tower[name]
    if not children:
        return wt
    return wt + sum(weight_of(x, tower) for x in children)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    60
    """
    tower = parse(text)
    root = find_root(tower)
    tgt_wt = None
    while True:
        weights = defaultdict(set)
        wt, children = tower[root]
        for x in children:
            weights[weight_of(x, tower)].add(x)
        if len(weights) == 1:
            return tgt_wt
        assert len(weights) == 2, weights
        other_name = None
        for wt, names in weights.items():
            if len(names) == 1:
                [name] = names
                bad_weight = wt
            else:
                other_wt = wt
                [other_name, *_] = names
        tgt_wt = tower[name][0] + other_wt - bad_weight
        root = name


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
