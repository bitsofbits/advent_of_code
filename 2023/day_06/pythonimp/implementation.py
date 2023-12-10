from math import ceil, floor, sqrt


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ([7, 15, 30], [9, 40, 200])
    """
    time_text, distance_text = text.strip().split('\n')
    times = [int(x) for x in time_text.split(":")[1].strip().split()]
    distances = [int(x) for x in distance_text.split(":")[1].strip().split()]
    return times, distances


def number_of_ways_to_win(race_time, best_distance):
    """
    d_max occurs where d/dc(c * (r - c)) == 0
    or r = 2c -> c = r / 2

    c * (r - c) = d when c**2 - c*r + d == 0
    => (r +- sqrt(r ** 2 - 4 * d)) / 2
    """
    lower_candidate = floor(
        (race_time - sqrt(race_time**2 - 4 * best_distance)) / 2.0
    )
    if lower_candidate * (race_time - lower_candidate) > best_distance:
        lower = lower_candidate
    else:
        lower = lower_candidate + 1
    assert lower * (race_time - lower) > best_distance

    upper_candidate = ceil((race_time + sqrt(race_time**2 - 4 * best_distance)) / 2.0)
    if upper_candidate * (race_time - upper_candidate) > best_distance:
        upper = upper_candidate
    else:
        upper = upper_candidate - 1
    assert upper * (race_time - upper) > best_distance

    return upper - lower + 1

    ways = 0
    for charge_time in range(1, race_time):
        run_time = race_time - charge_time
        distance = run_time * charge_time
        if distance > best_distance:
            ways += 1
    return ways


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    288
    """
    times, distances = parse(text)
    score = 1
    for t, d in zip(times, distances):
        score *= number_of_ways_to_win(t, d)
    return score


def parse_2(text):
    """
    >>> parse_2(EXAMPLE_TEXT)
    (71530, 940200)
    """
    time_text, distance_text = text.strip().split('\n')
    time = int(time_text.split(":")[1].strip().replace(' ', ''))
    distances = int(distance_text.split(":")[1].strip().replace(' ', ''))
    return time, distances


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    71503
    """
    time, distance = parse_2(text)
    return number_of_ways_to_win(time, distance)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
