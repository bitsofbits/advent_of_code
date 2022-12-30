from collections import defaultdict

EXAMPLE_TEXT = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


def parse(text):
    """
    >>> graph = parse(EXAMPLE_TEXT)
    >>> sorted((k, sorted(v)) for (k, v) in graph.items())[:2]
    [('DX', ['fs', 'he', 'pj', 'start']), ('RW', ['he', 'pj', 'start', 'zg'])]"""
    graph = defaultdict(set)
    for line in text.strip().split("\n"):
        a, b = line.split("-")
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    226
    """
    graph = parse(text)
    stack = [("start", set())]
    n_paths = 0
    while stack:
        lbl, visited = stack.pop()
        if lbl == "end":
            n_paths += 1
            continue
        # Can only visit lowercase labels once
        if lbl.isupper() or lbl not in visited:
            visited = visited | {lbl}
            for lbl in graph[lbl]:
                stack.append((lbl, visited))
    return n_paths


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    3509
    """
    graph = parse(text)
    stack = [("start", set(), 1)]
    n_paths = 0
    while stack:
        lbl, visited, scv_left = stack.pop()
        if lbl == "end":
            n_paths += 1
            continue
        # Can only visit lowercase labels once
        if lbl.isupper() or lbl not in visited or (scv_left > 0 and lbl != "start"):
            if not lbl.isupper() and lbl in visited:
                scv_left = scv_left - 1
            visited = visited | {lbl}
            for lbl in graph[lbl]:
                stack.append((lbl, visited, scv_left))
    return n_paths


if __name__ == "__main__":
    import doctest

    doctest.testmod()
