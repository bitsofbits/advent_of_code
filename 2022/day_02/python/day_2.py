play_score = {"X": 1, "Y": 2, "Z": 3}

results = {
    ("A", "X"): 3,
    ("A", "Y"): 6,
    ("A", "Z"): 0,
    ("B", "Y"): 3,
    ("B", "Z"): 6,
    ("B", "X"): 0,
    ("C", "Z"): 3,
    ("C", "X"): 6,
    ("C", "Y"): 0,
}


def score():
    total = 0
    for line in open("data/strategy_guide.txt"):
        if line.strip():
            op, me = line.split()
            total += play_score[me] + results[(op, me)]
    print("score", total)


me_map = {
    ("A", "X"): "Z",
    ("A", "Y"): "X",
    ("A", "Z"): "Y",
    ("B", "X"): "X",
    ("B", "Y"): "Y",
    ("B", "Z"): "Z",
    ("C", "X"): "Y",
    ("C", "Y"): "Z",
    ("C", "Z"): "X",
}


def score2():
    total = 0
    for line in open("data/strategy_guide.txt"):
        if line.strip():
            op, result = line.split()
            me = me_map[op, result]
            total += play_score[me] + results[(op, me)]
    print("score", total)


score()
score2()
