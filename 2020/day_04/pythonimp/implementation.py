def parse(text):
    for passport in text.strip().split("\n\n"):
        passport = passport.strip()
        fields = passport.split()
        yield [x.split(":") for x in fields]


# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)

required = set(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])


EXAMPLE_VALID = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

EXAMPLE_INVALID = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""


def is_height(x):
    try:
        v = int(x[:-2])
    except ValueError:
        return False
    if x.endswith("cm"):
        return 150 <= v <= 193
    if x.endswith("in"):
        return 59 <= v <= 76
    return False


eye_colors = set("amb blu brn gry grn hzl oth".split())


def is_valid(passport, strict=False):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    if strict:
        fields = set()
        for p in passport:
            match p:
                case ("byr", x) if (1920 <= int(x) <= 2002):
                    fields.add("byr")
                case ("iyr", x) if (2010 <= int(x) <= 2020):
                    fields.add("iyr")
                case ("eyr", x) if (2020 <= int(x) <= 2030):
                    fields.add("eyr")
                case ("hgt", x) if is_height(x):
                    fields.add("hgt")
                case ("hcl", x) if x.startswith("#") and len(x) == 7 and all(
                    y in "abcdef0123456789" for y in x[1:]
                ):
                    fields.add("hcl")
                case ("ecl", x) if x in eye_colors:
                    fields.add("ecl")
                case ("pid", x) if len(x) == 9 and all(y in "0123456789" for y in x):
                    fields.add("pid")
    else:
        fields = set(k for (k, v) in passport)
    return fields >= required


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    2
    """
    return sum(1 for p in parse(text) if is_valid(p))


def part_2(text):
    """
    >>> part_2(EXAMPLE_VALID)
    4
    >>> part_2(EXAMPLE_INVALID)
    0
    """
    return sum(1 for p in parse(text) if is_valid(p, True))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
