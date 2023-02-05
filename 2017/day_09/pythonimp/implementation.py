import re


def parse(text):
    return text.strip()


escapes = re.compile(r"!.?")
garbage = re.compile(r"<([^>]*)>")


def remove_garbage(x):
    """
    >>> remove_garbage("<>")
    'G'
    >>> remove_garbage("<random characters>")
    'G'
    >>> remove_garbage("<<<<>")
    'G'
    >>> remove_garbage("<{!>}>")
    'G'
    >>> remove_garbage("<!!>")
    'G'
    >>> remove_garbage("<!!!>>")
    'G'
    >>> remove_garbage('<{o"i!a,<{i<a>')
    'G'
    >>> remove_garbage("{{<ab>},{<ab>},{<ab>},{<ab>}}")
    '{{G},{G},{G},{G}}'
    >>> remove_garbage("{<{},{},{{}}>}")
    '{G}'
    >>> remove_garbage("{<a>,<a>,<a>,<a>}")  # Not sure about this
    '{G,G,G,G}'
    >>> remove_garbage("{{<!>},{<!>},{<!>},{<a>}}")
    '{{G}}'
    >>> remove_garbage("{{<!!>},{<!!>},{<!!>},{<!!>}}")
    '{{G},{G},{G},{G}}'
    """
    return garbage.sub("G", escapes.sub("", x))


def score_clean(x, level):
    if not x or (not x[0] in "{G"):
        return 0
    assert x[-1] in "}G"
    score = 0
    while x:
        if x[0] == "G":
            i = 0
        else:
            cnt = 0
            for i, c in enumerate(x):
                if c == "{":
                    cnt += 1
                if c == "}":
                    cnt -= 1
                if cnt <= 0:
                    break
            assert cnt == 0, (cnt, c, x)
            score += level + score_clean(x[1:i], level + 1)
        if i < len(x) - 1:
            i += 1
            assert x[i] == ",", (i, x)
        x = x[i + 1 :]
    return score


def score(x):
    """
    >>> score("{}")
    1
    >>> score("{{{}}}")
    6
    >>> score("{{},{}}")
    5
    >>> score("{{{},{},{{}}}}")
    16
    >>> score("{<a>,<a>,<a>,<a>}")
    1
    >>> score("{{<ab>},{<ab>},{<ab>},{<ab>}}")
    9
    >>> score("{{<a!>},{<a!>},{<a!>},{<ab>}}")
    3
    >>> score("{{<!!>},{<!!>},{<!!>},{<!!>}}")
    9
    """
    return score_clean(remove_garbage(x), 1)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    3
    """  # 10694 is too low
    return score(parse(text))


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    17
    """
    return sum(len(x) for x in garbage.findall(escapes.sub("", parse(text))))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
