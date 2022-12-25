def as_set(txt):
    beg, end = (int(x) for x in txt.split("-"))
    return set(range(beg, end + 1))


def load_assignments(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                yield tuple(as_set(x) for x in line.split(","))


def is_contained(sets):
    a, b = sets
    if not a - b:
        return True
    if not b - a:
        return True
    return False


def is_ovelapping(sets):
    a, b = sets
    return bool(a & b)


if __name__ == "__main__":
    assignments = list(load_assignments("data/assignments.txt"))
    n_contained = sum(is_contained(x) for x in assignments)
    print("number completely contained:", n_contained)
    n_overlap = sum(is_ovelapping(x) for x in assignments)
    print("number of overlaps:", n_overlap)
