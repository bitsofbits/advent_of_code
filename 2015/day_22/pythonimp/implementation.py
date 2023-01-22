from __future__ import annotations

import math
from heapq import heappop, heappush
from typing import NamedTuple


class Boss(NamedTuple):
    hit_points: int
    damage: int


class Mage(NamedTuple):
    hit_points: int = 50
    mana: int = 500
    armor: int = 0


class Spell(NamedTuple):
    name: str
    cost: int
    duration: int = 0
    damage: int = 0
    heal: int = 0
    recharge: int = 0
    armor: int = 0


spells = [
    Spell("Magic Missile", cost=53, damage=4),
    Spell("Drain", cost=73, damage=2, heal=2),
    Spell("Shield", cost=113, duration=6, armor=7),
    Spell("Poison", cost=173, duration=6, damage=3),
    Spell("Recharge", cost=229, duration=5, recharge=101),
]


def apply_effects(mage, boss, effects):
    new_effects = {}
    mage = mage._replace(armor=0)
    for spell, timer in effects.items():
        boss = boss._replace(hit_points=boss.hit_points - spell.damage)
        mage = Mage(
            mage.hit_points + spell.heal,
            mage.mana + spell.recharge,
            mage.armor + spell.armor,
        )
        timer -= 1
        if timer > 0:
            new_effects[spell] = timer
    return mage, boss, new_effects


def solve(boss, hard=False):
    mage = Mage()
    lowest_mana_cost = math.inf
    queue = [(boss, mage, 0, {})]
    while queue:
        boss, mage, mana_cost, effects = heappop(queue)
        # Player turn
        if hard:
            mage = mage._replace(hit_points=mage.hit_points - 1)
        mage, boss, effects = apply_effects(mage, boss, effects)
        if boss.hit_points <= 0:
            lowest_mana_cost = min(lowest_mana_cost, mana_cost)
            continue
        for s in spells:
            if s not in effects and mage.mana >= s.cost:
                next_mana_cost = mana_cost + s.cost
                if next_mana_cost >= lowest_mana_cost:
                    continue
                if s.duration == 0:
                    next_mage = mage._replace(
                        hit_points=mage.hit_points + s.heal, mana=mage.mana - s.cost
                    )
                    next_boss = boss._replace(hit_points=boss.hit_points - s.damage)
                    next_effects = effects
                else:
                    next_mage = mage._replace(mana=mage.mana - s.cost)
                    next_boss = boss
                    next_effects = effects.copy()
                    next_effects[s] = s.duration
                # Bosses turn
                next_mage, next_boss, next_effects = apply_effects(
                    next_mage, next_boss, next_effects
                )
                if next_boss.hit_points <= 0:
                    lowest_mana_cost = min(lowest_mana_cost, next_mana_cost)
                    continue
                next_mage = next_mage._replace(
                    hit_points=next_mage.hit_points
                    - (next_boss.damage - next_mage.armor)
                )
                if next_mage.hit_points > 0:
                    heappush(
                        queue, (next_boss, next_mage, next_mana_cost, next_effects)
                    )
    return lowest_mana_cost


def parse(text):
    """
    >>> parse(EXAMPLE_TEXT)
    Boss(hit_points=71, damage=10)
    """
    lines = text.strip().split("\n")
    hit_points = int(lines[0].split(": ")[-1])
    damage = int(lines[1].split(": ")[-1])
    return Boss(hit_points, damage)


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    1824
    """
    boss = parse(text)
    return solve(boss)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    1937
    """
    boss = parse(text)
    return solve(boss, hard=True)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "input.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
