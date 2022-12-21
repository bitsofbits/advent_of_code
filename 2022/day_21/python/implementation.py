import sys

example_text = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def parse_text(text):
    """
    >>> ns = parse_text(example_text)
    >>> for k, v in ns.items(): print(f"{k} : {v}")
    root : pppw + sjmn
    dbpl : 5
    cczh : sllz + lgvd
    zczc : 2
    ptdq : humn - dvpt
    dvpt : 3
    lfqf : 4
    humn : 5
    ljgn : 2
    sjmn : drzm * dbpl
    sllz : 4
    pppw : cczh / lfqf
    lgvd : ljgn * ptdq
    drzm : hmdt - zczc
    hmdt : 32
    """
    namespace = {}
    for line in text.strip().split("\n"):
        k, v = (x.strip() for x in line.split(": "))
        try:
            v = int(v.strip())
        except ValueError:
            pass
        namespace[k] = v
    return namespace


def monkey_eval(namespace, target="root", return_ordered=False):
    """
    >>> monkey_eval(parse_text(example_text))
    152
    """
    known_space = {}
    outer_space = {}
    for k, v in namespace.items():
        if isinstance(v, int):
            known_space[k] = v
        else:
            outer_space[k] = v
    ordered = known_space.copy()

    while True:
        if target in known_space:
            if return_ordered:
                return ordered
            else:
                return known_space[target]
        for k in list(outer_space):
            expr = outer_space[k]
            try:
                v = eval(expr, {}, known_space)
            except (NameError, TypeError):
                pass
            else:
                if isinstance(v, (int, float)):
                    if v % 1 == 0:
                        v = int(v)
                    known_space[k] = v
                    ordered[k] = expr
                    del outer_space[k]
                    break


def human_eval(namespace, low=0, high=10000000000000):
    # # low=3460000000000, high=3460000001000):
    # 1000000000000
    # 3460000001000
    """
    >>> human_eval(parse_text(example_text))
    301
    """
    namespace = monkey_eval(namespace, return_ordered=True)
    a, _, b = namespace["root"].split()
    namespace["root"] = f"{a} - {b}"

    def heval(x):
        namespace["humn"] = x
        return monkey_eval(namespace)

    # Assume monotonic
    L = heval(low)
    H = heval(high)
    while True:
        mid = (low + high) // 2
        M = heval(mid)
        if M == 0:
            return mid
        elif L * M < 0:
            # This contains our point
            high = mid
        elif M * H < 0:
            # nope this
            low = mid
        else:
            # :-(
            print(low, mid, high, L, M, H)
            raise ValueError("didn't converge")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    with open("data/data.txt") as f:
        text = f.read()
    namespace = parse_text(text)
    print(monkey_eval(namespace))
    print(human_eval(namespace))
