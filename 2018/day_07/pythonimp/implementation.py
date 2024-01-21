from collections import defaultdict
from heapq import heappop, heappush

# Step C must be finished before step A can begin.


def parse(text):
    """
    >>> len(parse(EXAMPLE_TEXT))
    5
    """
    requirements = defaultdict(set)
    for line in text.strip().split('\n'):
        _, src, *_, tgt, _, _ = line.split()
        requirements[tgt].add(src)
    return requirements


def find_all_inputs(requirements):
    nodes = set()
    for k, values in requirements.items():
        for v in values:
            nodes.add(v)
    return nodes


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    'CABDFE'
    """
    requirements = parse(text)
    inputs = find_all_inputs(requirements)
    required_by = {k: set() for k in inputs | set(requirements)}
    for k, values in requirements.items():
        for v in values:
            required_by[v].add(k)
    initial_inputs = inputs - set(requirements)
    sequence = []
    seen = set()
    queue = [(0, x) for x in initial_inputs]
    while queue:
        trial, node = heappop(queue)
        if node in seen:
            continue
        if requirements[node] - seen:
            # Can't process yet, so stick back on stack
            heappush(queue, (trial + 1, node))
            continue
        seen.add(node)
        sequence.append(node)
        for child in required_by[node]:
            heappush(queue, (0, child))
    return ''.join(sequence)


def part_2(
    text, nominal_order='OUGLTKDJVBRMIXSACWYPEQNHZF', base_seconds=60, n_workers=5
):
    """
    >>> part_2(EXAMPLE_TEXT, 'CABDFE', 0, 2)
    15

    OUGLTKDJVBRMIXSACWYPEQNHZF
    """
    requirements = parse(text)
    workers = {i: (None, None) for i in range(n_workers)}
    complete = set()
    in_progress = set()
    t = 0
    while len(complete) < len(nominal_order):
        # Allow workers to finish up
        for worker, (project, finish_time) in workers.items():
            if project is not None:
                assert finish_time >= t
                if finish_time == t:
                    complete.add(project)
                    in_progress.remove(project)
                    workers[worker] = (None, None)

        if len(complete) == len(nominal_order):
            break

        # Assign available workers to new projects
        for worker, (project, finish_time) in workers.items():
            if project is None:
                for new_project in nominal_order:
                    if (
                        new_project not in complete | in_progress
                        and not requirements[new_project] - complete
                    ):
                        new_time = t + base_seconds + (ord(new_project) - ord('A') + 1)
                        workers[worker] = (new_project, new_time)
                        in_progress.add(new_project)
                        break
        t += 1
    return t


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
