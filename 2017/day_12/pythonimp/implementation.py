from collections import defaultdict


def parse(text):
    """
    >>> len(parse(EXAMPLE_TEXT))
    """
    graph = defaultdict(set)
    for line in text.strip().split("\n"):
        src, targets = (x.strip() for x in line.split("<->"))
        src = int(src)
        for tgt in targets.split(","):
            tgt = int(tgt.strip())
            graph[src].add(tgt)
            graph[tgt].add(src)
    return dict(graph)


def find_connected(graph, start=0):
    stack = [start]
    seen = set([start])
    while stack:
        nd = stack.pop()
        for next_nd in graph[nd]:
            if next_nd not in seen:
                seen.add(next_nd)
                stack.append(next_nd)
    return seen


def find_all_groups(graph):
    n_nodes = len(graph)
    seen = set()
    while len(seen) < n_nodes:
        for start in graph:
            if start not in seen:
                break
        group = find_connected(graph, start)
        yield group
        seen |= group


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    6
    """
    graph = parse(text)
    return len(find_connected(graph))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    2
    """
    graph = parse(text)
    return sum(1 for _ in find_all_groups(graph))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
