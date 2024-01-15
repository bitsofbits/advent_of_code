def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)[:10]
    (8, 0, 8, 7, 1, 2, 2, 4, 5, 8)
    """
    return tuple([int(x) for x in text.strip()])


base_pattern = [0, 1, 0, -1]


def render(signal):
    return ''.join(str(x) for x in signal)


def raw_compute_next_phase(signal, shift=1, n=None):
    if n is None:
        n = len(signal)
    output = [None] * n
    for i in range(n):
        output[i] = sum(
            x * base_pattern[((j + shift) // (i + 1)) % 4]
            for (j, x) in enumerate(signal)
        )
    return output


# Y_i = sum(X_j * P[(j // i) % 4])
# Y_i = sum(X_2j * P[(2 * j // i) % 4]) + sum(X_2j+1 * P[((2 * j + 1) // i) % 4])  # i = 1,...,N


def compute_next_phase(signal):
    """
    >>> signal = parse('12345678')
    >>> render(signal)
    '12345678'
    >>> signal = compute_next_phase(signal)
    >>> render(signal)
    '48226158'
    >>> signal = compute_next_phase(signal)
    >>> render(signal)
    '34040438'
    """
    raw_output = raw_compute_next_phase(signal)
    return [abs(x) % 10 for x in raw_output]


def part_1(text, phases=100):
    """
    >>> part_1('69317163492948606335995924319873', phases=100)
    '52432133'
    """
    signal = parse(text)
    for _ in range(phases):
        signal = compute_next_phase(signal)
    return render(signal[:8])


def compute_next_half_phase(partial_signal):
    # As long as we're past the halfway point, we can compute just sum from the
    # diagonal onward. And it never depends on stuff in the first half.
    output = []
    total = 0
    for x in reversed(partial_signal):
        total += x
        output.append(total)
    return [abs(x) % 10 for x in output[::-1]]


def part_2(text):
    """
    >>> part_2('03036732577212944063491565474664')
    '84462026'
    >>> part_2('02935109699940807407585447034323')
    '78725270'
    """
    base_signal = parse(text)
    message_offset = int(render(base_signal[:7]))
    full_signal = base_signal * 10_000
    assert message_offset > len(full_signal) // 2
    partial_signal = full_signal[message_offset:]
    for _ in range(100):
        partial_signal = compute_next_half_phase(partial_signal)
    return render(partial_signal[:8])


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    with open(data_dir / "input.txt") as f:
        INPUT_TEXT = f.read()

    doctest.testmod()
