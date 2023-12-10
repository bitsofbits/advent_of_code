import re


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
    """
    return text.strip().split('\n')


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    142
    """
    total = 0
    for line in parse(text):
        for x in line:
            if x in '0123456789':
                total += 10 * int(x)
                break
        for x in line[::-1]:
            if x in '0123456789':
                total += int(x)
                break
    return total


EXAMPLE2_TEXT = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


digits = "[0123456789]"
digit_words = "one|two|three|four|five|six|seven|eight|nine|zero"
pattern = digits + '|' + digit_words
reversed_pattern = digits + '|' + digit_words[::-1]
digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
}


def find_number(line):
    key = re.search(pattern, line).group()
    x1 = int(digit_map.get(key, key))
    match = re.search(reversed_pattern, line[::-1])
    key = match.group()[::-1]
    x2 = int(digit_map.get(key, key))
    return 10 * x1 + x2


def part_2(text):
    """
    >>> part_2(EXAMPLE2_TEXT)
    281
    """
    total = 0
    for line in parse(text):
        total += find_number(line)
    return total


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
