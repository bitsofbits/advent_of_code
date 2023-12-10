import re


def find_symbols(lines):
    for row, line in enumerate(lines):
        for col, x in enumerate(line):
            if x not in '.0123456789':
                yield x, (row, col)


def build_symbol_map(symbols):
    symbol_map = set()
    for x, (i, j) in symbols:
        symbol_map.add((i, j))
    return symbol_map


def pad_symbol_map(symbol_map):
    padded_map = set()
    for i, j in symbol_map:
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                padded_map.add((i + di, j + dj))
    return padded_map


def find_numbers(lines):
    for row, line in enumerate(lines):
        for match in re.finditer('[0123456789]+', line):
            yield int(match.group()), row, match.span()


def parse(text):
    """
    >>> numbers, symbol_map = parse(EXAMPLE_TEXT)
    """
    lines = [x.strip() for x in text.strip().split('\n')]
    symbol_map = build_symbol_map(find_symbols(lines))
    number_info = list(find_numbers(lines))
    return number_info, symbol_map


def valid_numbers(number_info, padded_symbol_map):
    for x, row, span in number_info:
        for col in range(*span):
            if (row, col) in padded_symbol_map:
                yield x
                break


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    4361

    # 556367 for full data
    """
    number_info, symbol_map = parse(text)
    padded_map = pad_symbol_map(symbol_map)
    return sum(valid_numbers(number_info, padded_map))


def gear_ratios(number_info, symbol_map):
    gear_map = {k: [] for k in symbol_map}
    for x, i, span in number_info:
        symbols_seen = set()
        for j in range(*span):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    key = (i + di, j + dj)
                    if key in symbol_map and key not in symbols_seen:
                        symbols_seen.add(key)
                        gear_map[key].append(x)
    for numbers in gear_map.values():
        if len(numbers) == 2:
            a, b = numbers
            yield a * b


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    467835

    # 88373022 is too low for all values
    """
    number_info, symbol_map = parse(text)
    return sum(gear_ratios(number_info, symbol_map))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
