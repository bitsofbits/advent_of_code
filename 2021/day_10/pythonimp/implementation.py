EXAMPLE_TEXT = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

CORRUPT_SCORE = {")": 3, "]": 57, "}": 1197, ">": 25137}
MATCH = {"(": ")", "[": "]", "{": "}", "<": ">"}


def check(line):
    """
    >>> for line in EXAMPLE_TEXT.strip().split("\\n"): print(check(line))
    None
    None
    }
    None
    )
    ]
    None
    )
    >
    None
    """
    stack = []
    for c in line:
        if c in "<{([":
            stack.append(c)
        elif c != MATCH[stack.pop()]:
            return c
    return None


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    26397
    """
    total = 0
    for line in text.strip().split("\n"):
        total += CORRUPT_SCORE.get(check(line), 0)
    return total


def repair(line):
    """
    >>> repair("[({(<(())[]>[[{[]{<()<>>")
    '}}]])})]'
    """
    stack = []
    for c in line:
        if c in "<{([":
            stack.append(c)
        else:
            assert c == MATCH[stack.pop()]
    return "".join(MATCH[x] for x in stack[::-1])


REPAIR_SCORE = {")": 1, "]": 2, "}": 3, ">": 4}


def repair_score(repair):
    score = 0
    for x in repair:
        score *= 5
        score += REPAIR_SCORE[x]
    return score


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    288957
    """
    lines = text.strip().split("\n")
    repairs = [repair(x) for x in lines if check(x) is None]
    scores = [repair_score(x) for x in repairs]
    scores.sort()
    return scores[len(scores) // 2]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
