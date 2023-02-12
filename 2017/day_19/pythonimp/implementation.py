def parse(text):
    """
    >>> board, j = parse(EXAMPLE_TEXT)
    >>> j
    5
    """
    top_crd = None
    board = {}
    for i, line in enumerate(text.rstrip().split("\n")):
        for j, c in enumerate(line):
            if c != " ":
                board[i, j] = c
                if i == 0:
                    assert top_crd is None
                    top_crd = j
    return board, top_crd


def traverse(board, j):
    i = 0
    assert board[i, j] == "|"
    seen = []
    count = 0
    d = "D"
    while (i, j) in board:
        c = board[i, j]
        count += 1
        if "A" <= c <= "Z":
            seen.append(c)
        match d, c:
            case "D" | "U", "+":
                for delta, x in ((-1, "L"), (1, "R")):
                    if board.get((i, j + delta), "|") != "|":
                        j += delta
                        d = x
                        break
            case "L" | "R", "+":
                for delta, x in ((-1, "U"), (1, "D")):
                    if board.get((i + delta, j), "-") != "-":
                        i += delta
                        d = x
                        break
            case "D", x:
                i += 1
            case "U", x:
                i -= 1
            case "R", x:
                j += 1
            case "L", x:
                j -= 1
            case _:
                raise ValueError((d, c))
    return "".join(seen), count


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    'ABCDEF'
    """
    board, j = parse(text)
    seen, steps = traverse(board, j)
    return seen


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    38
    """
    board, j = parse(text)
    seen, steps = traverse(board, j)
    return steps


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
