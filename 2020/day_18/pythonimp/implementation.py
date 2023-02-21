def tokenize(text):
    """
    >>> for x in tokenize(EXAMPLE_TEXT): print(x[:8])
    ['1', '+', '2', '*', '3', '+', '4', '*']
    ['2', '*', '3', '+', '(', '4', '*', '5']
    ['5', '+', '(', '8', '*', '3', '+', '9']
    ['5', '*', '9', '*', '(', '7', '*', '3']
    ['(', '(', '2', '+', '4', '*', '9', ')']
    """
    for line in text.strip().split("\n"):
        line = line.strip().replace("(", " ( ").replace(")", " ) ")
        yield line.split()


def evaluate(tokens):
    """
    >>> for tokens in tokenize(EXAMPLE_TEXT): print(evaluate(tokens))
    71
    26
    437
    12240
    13632
    """
    N = len(tokens)
    i = 0
    value = None
    last_op = "="

    def apply_val(x):
        nonlocal value, last_op
        match last_op:
            case "=":
                value = x
            case "*":
                value *= x
            case "+":
                value += x
            case _:
                raise ValueError(last_op)
        last_op = None

    while i < N:
        match tokens[i]:
            case "(":
                subtokens = []
                cnt = 1
                for j in range(i + 1, N):
                    if tokens[j] == "(":
                        cnt += 1
                    if tokens[j] == ")":
                        cnt -= 1
                    if cnt == 0:
                        break
                    subtokens.append(tokens[j])
                i = j
                apply_val(evaluate(subtokens))
            case "*":
                last_op = "*"
            case "+":
                last_op = "+"
            case x:
                apply_val(int(x))
        i += 1
    return value


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    26406
    """
    total = 0
    for tokens in tokenize(text):
        total += evaluate(tokens)
    return total


def evaluate2(tokens):
    """
    >>> for tokens in tokenize(EXAMPLE_TEXT): print(evaluate2(tokens))
    231
    46
    1445
    669060
    23340
    """
    N = len(tokens)
    i = 0
    value = None
    last_op = "="

    def apply_val(x):
        nonlocal value, last_op
        match last_op:
            case "=":
                value = x
            case "*":
                value *= x
            case "+":
                value += x
            case None:
                pass  # why?
            case _:
                print("ERROR", last_op, value)
        last_op = None

    while i < N:
        match tokens[i]:
            case "(":
                subtokens = []
                cnt = 1
                for j in range(i + 1, N):
                    if tokens[j] == "(":
                        cnt += 1
                    if tokens[j] == ")":
                        cnt -= 1
                    if cnt == 0:
                        break
                    subtokens.append(tokens[j])
                i = j
                apply_val(evaluate2(subtokens))
            case "*":
                subtokens = []
                cnt = 0
                for j in range(i + 1, N):
                    if tokens[j] == "(":
                        cnt += 1
                    if tokens[j] == ")":
                        cnt -= 1
                    if cnt == 0 and tokens[j] == "*":
                        break
                    subtokens.append(tokens[j])
                else:
                    j += 1
                i = j - 1
                last_op = "*"
                # print(">>>", subtokens)
                apply_val(evaluate2(subtokens))
            case "+":
                last_op = "+"
            case x:
                try:
                    apply_val(int(x))
                except:
                    print("Error", i, repr(x))
                    print(tokens)
        i += 1
    return value


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    694122
    """
    total = 0
    for tokens in tokenize(text):
        total += evaluate2(tokens)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
