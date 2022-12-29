EXAMPLE_TEXT = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
"""

#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....

#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg


NUMBERS = {
    frozenset("abcefg"): 0,
    frozenset("cf"): 1,
    frozenset("acdeg"): 2,
    frozenset("acdfg"): 3,
    frozenset("bcdf"): 4,
    frozenset("abdfg"): 5,
    frozenset("abdefg"): 6,
    frozenset("acf"): 7,
    frozenset("abcdefg"): 8,
    frozenset("abcdfg"): 9,
}
SEGMENTS = {v: k for (k, v) in NUMBERS.items()}

ALL = frozenset("abcdefg")


SEGS_BY_LEN = {i: frozenset(k for k in NUMBERS if len(k) == i) for i in range(10)}


def clean(text):
    """
    >>> print(clean(EXAMPLE_TEXT).split("\\n")[0])
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    """
    return text.strip().replace("|\n", "| ")


def parse(line):
    """
    >>> p, o = parse(clean(EXAMPLE_TEXT).split("\\n")[0])
    >>> sorted([sorted(x) for x in p])[:2]
    [['a', 'b', 'c', 'd', 'e', 'f', 'g'], ['a', 'b', 'c', 'd', 'f']]
    >>> [sorted(x) for x in o[:2]]
    [['a', 'b', 'c', 'd', 'e', 'f', 'g'], ['b', 'c', 'd', 'e', 'f']]
    """
    patterns, out = line.split("|")
    patterns = frozenset(frozenset(x) for x in patterns.split())
    out = [frozenset(x) for x in out.split()]
    return patterns, out


def count_1478(line):
    """
    >>> count_1478(clean(EXAMPLE_TEXT).split("\\n")[0])
    2
    """
    patterns, out = parse(line)
    targets = [1, 4, 7, 8]
    tgt_lens = set()
    for x in targets:
        n = len(SEGMENTS[x])
        assert len(SEGS_BY_LEN[n]) == 1, (x, n, SEGS_BY_LEN[n])
        tgt_lens.add(n)
    tgt_patterns = {x for x in patterns if len(x) in tgt_lens}
    return sum(x in tgt_patterns for x in out)

    return patterns, [len(SEGS_BY_LEN[len(x)]) for x in patterns]


def part_1(text):
    """
    >>> part_1(clean(EXAMPLE_TEXT))
    26
    """
    return sum(count_1478(line) for line in text.strip().split("\n"))


def decode(line):
    """
    >>> decode(clean(EXAMPLE_TEXT).split("\\n")[0])
    8394
    """
    patterns, out = parse(line)
    pat = [None] * 10
    [pat[1]] = [p for p in patterns if len(p) == 2]
    [pat[4]] = [p for p in patterns if len(p) == 4]
    [pat[7]] = [p for p in patterns if len(p) == 3]
    [pat[8]] = [p for p in patterns if len(p) == 7]

    [pat[2]] = [p for p in patterns if len(p) == 5 and (len(p & pat[4]) == 2)]
    [pat[3]] = [p for p in patterns if len(p) == 5 and len(p & pat[1]) == 2]
    [pat[5]] = [p for p in patterns if len(p) == 5 and p not in {pat[2], pat[3]}]
    [pat[6]] = [p for p in patterns if len(p) == 6 and len(p - pat[1]) == 5]
    [pat[9]] = [p for p in patterns if len(p) == 6 and len(p & pat[4]) == 4]
    [pat[0]] = [p for p in patterns if len(p) == 6 and p not in {pat[6], pat[9]}]

    assert set(pat) == set(patterns), set(patterns) - set(pat)

    decoder = {x: i for (i, x) in enumerate(pat)}
    return sum([decoder[x] * 10**i for (i, x) in enumerate(out[::-1])])


def part_2(text):
    """
    >>> part_2(clean(EXAMPLE_TEXT))
    61229
    """
    return sum(decode(line) for line in text.strip().split("\n"))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
