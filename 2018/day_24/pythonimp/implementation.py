# 17 units each with 5390 hit points (weak to radiation, bludgeoning) with
#  an attack that does 4507 fire damage at initiative 2

# 17 units each with 5390 hit points (weak to radiation, bludgeoning) with
#  an attack that does 4507 fire damage at initiative 2
from dataclasses import dataclass


@dataclass
class Group:
    army: str
    n_units: int
    hit_points: int
    weaknesses: tuple[str]
    immunities: tuple[str]
    attack_damage: int
    attack_type: str
    initiative: int

    @property
    def effective_power(self):
        return self.n_units * self.attack_damage

    def __hash__(self):
        return id(self)


def parse_weaknesses(x):
    # return x
    chunks = x.split(';')
    weaknesses = {'immune': (), 'weak': ()}
    for chunk in chunks:
        kind, _, chunk = chunk.split(maxsplit=2)
        weaknesses[kind] = tuple(sorted(x.strip() for x in chunk.split(',')))
    return weaknesses


def parse_group(line, army):
    n_units, _, _, _, hit_points, line = line.split(maxsplit=5)
    n_units = int(n_units)
    hit_points = int(hit_points)
    assert line.startswith('hit points')
    if '(' in line:
        _, line = line.split('(', maxsplit=1)
        weaknesses, line = line.split(')', maxsplit=1)
        weaknesses = parse_weaknesses(weaknesses)
    else:
        _, line = line.split('hit points')
        weaknesses = {'immune': (), 'weak': ()}
    _, _, _, _, _, attack, attack_type, _, _, _, initiative = line.strip().split()
    attack = int(attack)
    initiative = int(initiative)
    return Group(
        army=army,
        n_units=n_units,
        hit_points=hit_points,
        weaknesses=weaknesses['weak'],
        immunities=weaknesses['immune'],
        attack_damage=attack,
        attack_type=attack_type,
        initiative=initiative,
    )


def parse(text):
    """
    >>> immune, infection = parse(EXAMPLE_TEXT)
    """
    immune_text, infection_text = text.strip().split('\n\n')
    immune_lines = immune_text.split('\n')
    assert immune_lines[0] == 'Immune System:'
    immune = [parse_group(x, army='immune') for x in immune_lines[1:]]
    infection_lines = infection_text.split('\n')
    assert infection_lines[0] == 'Infection:', infection_lines[0]
    infection = [parse_group(x, army='infection') for x in infection_lines[1:]]
    return immune, infection


def compute_damage(attacker, defender):
    if attacker.attack_type in defender.weaknesses:
        multiplier = 2
    elif attacker.attack_type in defender.immunities:
        multiplier = 0
    else:
        multiplier = 1
    return multiplier * attacker.effective_power


def select(attackers, targets):
    selections = []
    selected = set()
    for attacker in sorted(
        attackers, key=lambda x: (x.effective_power, x.initiative), reverse=True
    ):
        best_target = None
        max_key = (0, 0, 0)
        for target in targets:
            if target in selected:
                continue
            damage = compute_damage(attacker, target)
            key = (damage, target.effective_power, target.initiative)
            if damage > 0 and key > max_key:
                best_target = target
                max_key = key
        selected.add(best_target)
        max_damage, _, _ = max_key
        if max_damage > 0:
            selections.append((attacker, best_target))
    return selections


def simulate(text, boost):
    immune_system, infection = parse(text)
    for group in immune_system:
        group.attack_damage += boost
    while immune_system and infection:
        immune_selections = select(immune_system, infection)
        infection_selections = select(infection, immune_system)

        selections = sorted(
            immune_selections + infection_selections,
            key=lambda x: x[0].initiative,
            reverse=True,
        )

        units_killed = 0
        for attacker, target in selections:
            if attacker.n_units > 0:
                damage = compute_damage(attacker, target)
                n_killed = damage // target.hit_points
                target.n_units -= n_killed
                units_killed += n_killed

        if not units_killed:
            break

        immune_system = [x for x in immune_system if x.n_units > 0]
        infection = [x for x in infection if x.n_units > 0]
    return immune_system, infection


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    5216
    """
    immune_system, infection = simulate(text, boost=0)
    return sum(x.n_units for x in immune_system + infection)


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    51

    677 is too low!
    """
    low = 0
    high = 2048
    immune_system, infection = simulate(text, boost=high)
    assert immune_system
    while low < high:
        middle = (low + high) // 2
        if middle in (low, high):
            break
        immune_system, infection = simulate(text, boost=middle)
        if not infection:
            high = middle
        else:
            low = middle
    immune_system, infection = simulate(text, boost=high)
    assert immune_system and not infection
    return sum(x.n_units for x in immune_system)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
