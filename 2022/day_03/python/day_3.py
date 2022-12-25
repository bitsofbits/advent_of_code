def load_rucksacks(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield line


def split_into_compartments(rucksacks):
    for line in rucksacks:
        n = len(line)
        assert n % 2 == 0
        yield line[: n // 2], line[n // 2 :]


def find_duplicates(contents):
    for items in contents:
        dups = None
        for x in items:
            if dups is None:
                dups = set(x)
            else:
                dups &= set(x)
        [dup] = dups
        yield dup


def find_scores(duplicates):
    for dup in duplicates:
        if "a" <= dup <= "z":
            yield ord(dup) - ord("a") + 1
        elif "A" <= dup <= "Z":
            yield ord(dup) - ord("A") + 27
        else:
            raise ValueError(f'"{dup}" not in a..z or A..Z')


def as_triples(items):
    chunk = []
    for x in items:
        chunk.append(x)
        if len(chunk) == 3:
            yield chunk
            chunk = []
    if chunk:
        raise ValueError("length of items not divisible by 3")


if __name__ == "__main__":
    path = "data/rucksack_contents.txt"

    total_score = sum(
        find_scores(find_duplicates(split_into_compartments(load_rucksacks(path))))
    )
    print("priority score =", total_score)

    badge_score = sum(find_scores(find_duplicates(as_triples(load_rucksacks(path)))))
    print("badge_score =", badge_score)
