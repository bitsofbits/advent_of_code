from collections import defaultdict
from datetime import datetime, timedelta


def parse_line(line):
    timestamp_str, action = line[1:].split('] ')
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
    return timestamp, action


def parse(text):
    """
    >>> for action in list(parse(EXAMPLE_TEXT))[:5]: print(action)
    (datetime.datetime(1518, 11, 1, 0, 0), 'Guard #10 begins shift')
    (datetime.datetime(1518, 11, 1, 0, 5), 'falls asleep')
    (datetime.datetime(1518, 11, 1, 0, 25), 'wakes up')
    (datetime.datetime(1518, 11, 1, 0, 30), 'falls asleep')
    (datetime.datetime(1518, 11, 1, 0, 55), 'wakes up')
    """
    for line in text.strip().split('\n'):
        yield parse_line(line)


def compile_records(records):
    records = sorted(records)
    minutes = defaultdict(lambda: [0] * 60)
    guard = None
    fell_asleep = None
    for time, action in records:
        if action.startswith('Guard'):
            guard = int(action.split()[1][1:])
            assert fell_asleep is None
            fell_asleep = None
        elif action.startswith('falls'):
            fell_asleep = time.minute
        elif action.startswith('wakes'):
            for i in range(fell_asleep, time.minute):
                minutes[guard][i] += 1
            fell_asleep = None
        else:
            raise ValueError(action)
    return dict(minutes)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    240

    94048 is too high :-(
    """
    minutes = compile_records(parse(text))
    minutes_per_guard = {guard: sum(rng) for (guard, rng) in minutes.items()}
    sleepiest_guard = max(minutes_per_guard, key=lambda x: minutes_per_guard[x])
    sleepiest_minute = max(range(60), key=lambda x: minutes[sleepiest_guard][x])
    return sleepiest_guard * sleepiest_minute


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    4455
    """
    minutes = compile_records(parse(text))
    max_count = 0
    best_result = None
    for guard, minutes in minutes.items():
        for minutes, count in enumerate(minutes):
            if count > max_count:
                max_count = count
                best_result = minutes * guard
    return best_result


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
