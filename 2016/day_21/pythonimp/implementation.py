from itertools import permutations


def parse(text):
    # Could speed this up by doing more work here, parsing down to single
    # commands and args instead of doing the work in scramble
    for line in text.strip().split("\n"):
        match line.split():
            case ("swap", "position", X, "with", "position", Y):
                i, j = (int(v) for v in [X, Y])
                yield "SWAPPOS", i, j
            case ("swap", "letter", X, "with", "letter", Y):
                i, j = (text.index(v) for v in [X, Y])
                yield "SWAPLET", X, Y
            case ("rotate", "left", X, "steps" | "step"):
                n = int(X)
                if n > 0:
                    yield "ROTATELEFT", int(X)
            case ("rotate", "right", X, "steps" | "step"):
                n = int(X)
                if n > 0:
                    yield "ROTATERIGHT", int(X)
            case ("rotate", "based", "on", "position", "of", "letter", X):
                yield "ROTATEPOS", X
            case ("reverse", "positions", X, "through", Y):
                i, j = (int(v) for v in [X, Y])
                assert j >= i
                yield "REVERSE", i, j + 1
            case ("move", "position", X, "to", "position", Y):
                i, j = (int(v) for v in [X, Y])
                yield "MOVE", i, j
            case _:
                raise ValueError(x)


def scramble(text, steps):
    """
    >>> steps = parse(EXAMPLE_TEXT)
    >>> scramble("abcde", steps)
    'decab'
    """
    text = list(text)
    for x in steps:
        match x:
            case "SWAPPOS", i, j:
                text[i], text[j] = text[j], text[i]
            case "SWAPLET", X, Y:
                i, j = (text.index(v) for v in [X, Y])
                text[i], text[j] = text[j], text[i]
            case "ROTATERIGHT", n:
                text = text[-n:] + text[:-n]
            case "ROTATELEFT", n:
                text = text[n:] + text[:n]
            case "ROTATEPOS", X:
                n = text.index(X)
                if n >= 4:
                    n += 1
                n += 1
                n %= len(text)
                if n > 0:
                    text = text[-n:] + text[:-n]
            case "REVERSE", i, j:
                text[i:j] = reversed(text[i:j])
            case "MOVE", i, j:
                c = text.pop(i)
                text.insert(j, c)
            case _:
                raise ValueError(x)

    return "".join(text)


def part_1(text, seed="abcdefgh"):
    """
    >>> part_1(EXAMPLE_TEXT, "abcde")
    'decab'
    """
    steps = parse(text)
    return scramble(seed, steps)


def part_2(text, target="fbgdceah"):
    steps = list(parse(text))
    for x in permutations(target):
        if scramble(x, steps) == target:
            return "".join(x)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
