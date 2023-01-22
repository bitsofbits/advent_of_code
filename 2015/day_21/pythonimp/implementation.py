from __future__ import annotations

from typing import NamedTuple


class Stats(NamedTuple):
    hit_points: int
    damage: int
    armor: int


class Item(NamedTuple):
    name: str
    kind: str
    cost: int
    damage: int
    armor: int


class Loadout(NamedTuple):
    cost: int
    damage: int
    armor: int


items_str = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


def parse_items(text):
    items = []
    for chunk in items_str.strip().split("\n\n"):
        lines = chunk.strip().split("\n")
        kind = lines[0].split(":")[0]
        if kind.endswith("s"):
            kind = kind[:-1]
        for line in lines[1:]:
            name, cost, damage, armor = line.strip().rsplit(maxsplit=3)
            items.append(Item(name, kind, int(cost), int(damage), int(armor)))
    return items


def create_equipment_combos():
    items = parse_items(items_str)
    # 1 weapon
    weapons = [(x,) for x in items if x.kind == "Weapon"]
    # 0 or 1 pieces of armor
    armor = [()] + [(x,) for x in items if x.kind == "Armor"]
    # 0, 1, or 2 rings
    ring_items = [x for x in items if x.kind == "Ring"]
    rings = [()]
    for a in ring_items:
        rings.append((a,))
        for b in ring_items:
            if a.name != b.name:
                rings.append((a, b))

    loads = set()
    for w in weapons:
        for a in armor:
            for r in rings:
                stuff = w + a + r
                load = Loadout(
                    cost=sum(x.cost for x in stuff),
                    damage=sum(x.damage for x in stuff),
                    armor=sum(x.armor for x in stuff),
                )
                loads.add(load)
    return loads


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    Stats(hit_points=104, damage=8, armor=1)
    """
    lines = text.strip().split("\n")
    hit_points = int(lines[0].split(": ")[-1])
    damage = int(lines[1].split(": ")[-1])
    armor = int(lines[2].split(": ")[-1])
    return Stats(hit_points, damage, armor)


def i_win(me, boss):
    while True:
        d = max(me.damage - boss.armor, 1)
        boss = Stats(boss.hit_points - d, boss.damage, boss.armor)
        if boss.hit_points <= 0:
            return True
        d = max(boss.damage - me.armor, 1)
        me = Stats(me.hit_points - d, me.damage, me.armor)
        if me.hit_points <= 0:
            return False


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    78
    """
    boss = parse(text)
    loadouts = sorted(create_equipment_combos(), key=lambda x: x.cost)
    for x in loadouts:
        me = Stats(hit_points=100, damage=x.damage, armor=x.armor)
        if i_win(me, boss):
            return x.cost
    raise ValueError("no loadout works?")


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    148
    """
    boss = parse(text)
    loadouts = sorted(create_equipment_combos(), key=lambda x: x.cost, reverse=True)
    for x in loadouts:
        me = Stats(hit_points=100, damage=x.damage, armor=x.armor)
        if not i_win(me, boss):
            return x.cost
    raise ValueError("no loadout works?")


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
