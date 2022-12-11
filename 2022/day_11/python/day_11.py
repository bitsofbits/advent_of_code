import sys

from implementation import create_monkeys, play_round, read_text

if __name__ == "__main__":
    args = sys.argv[1:]
    (path,) = args

    text = read_text(path)
    monkeys = create_monkeys(text, 3)
    for _ in range(20):
        play_round(monkeys)

    for k, v in monkeys.items():
        print(k, v.items)

    for k, v in monkeys.items():
        print(k, v.cumulative_inspections)

    ordered = sorted(monkeys, key=lambda k: monkeys[k].cumulative_inspections)
    print(ordered)
    print(
        monkeys[ordered[-1]].cumulative_inspections
        * monkeys[ordered[-2]].cumulative_inspections
    )

    monkeys = create_monkeys(text, 1)
    for _ in range(10000):
        play_round(monkeys)
    for k, v in monkeys.items():
        print(k, v.cumulative_inspections)
    ordered = sorted(monkeys, key=lambda k: monkeys[k].cumulative_inspections)
    print(ordered)
    print(
        monkeys[ordered[-1]].cumulative_inspections
        * monkeys[ordered[-2]].cumulative_inspections
    )
