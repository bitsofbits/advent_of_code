def load_text(path):
    """
    >>> text = load_text("../data/input.txt")
    >>> len(text.strip())
    8192
    """
    with open(path) as f:
        return f.read()


def solve_1(text):
    """
    >>> solve_1(">")
    2
    >>> solve_1("^>v<")
    4
    >>> solve_1("^v^v^v^v^v")
    2
    >>> solve_1(load_text("../data/input.txt"))
    2565


    >>> 11 % 5
    >>> 10 % 5
    """
    board = set([(0, 0)])
    i = 0
    j = 0
    for c in text:
        match c:
            case ">":
                j += 1
            case "<":
                j -= 1
            case "^":
                i -= 1
            case "v":
                i += 1
            case _:
                raise ValueError(f"unexpected symbol: '{c}'")
        board.add((i, j))
    return len(board)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
