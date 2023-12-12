def parse_line(x):
    ingredients, allergens = x[:-1].split("(contains")
    ingredients = tuple(ingredients.strip().split())
    allergens = tuple(x.strip() for x in allergens.split(","))
    return ingredients, allergens


def parse(text):
    """
    >>> for x in parse(EXAMPLE_TEXT): print(x)
    (('mxmxvkd', 'kfcds', 'sqjhc', 'nhms'), ('dairy', 'fish'))
    (('trh', 'fvjkl', 'sbzzf', 'mxmxvkd'), ('dairy',))
    (('sqjhc', 'fvjkl'), ('soy',))
    (('sqjhc', 'mxmxvkd', 'sbzzf'), ('fish',))
    """
    for line in text.strip().split("\n"):
        yield parse_line(line)


def match_allergans(items):
    possible_foods = {}
    for ingredients, allergens in items:
        for k in allergens:
            if k not in possible_foods:
                possible_foods[k] = set(ingredients)
            else:
                possible_foods[k] &= set(ingredients)
    return full_match(possible_foods)


def update_known(alergen_to_food, known):
    changed = False
    for allergen, foods in alergen_to_food.items():
        if len(foods) == 1:
            [f] = foods
            known[allergen] = f
            changed = True
    for allergen in known:
        if allergen in alergen_to_food:
            changed = True
            alergen_to_food.pop(allergen)
    known_foods = set(known.values())
    for foods in alergen_to_food.values():
        overlap = known_foods & foods
        for x in overlap:
            changed = True
            foods.remove(x)
    return changed


# mxmxvkd contains dairy.
# sqjhc contains fish.
# fvjkl contains soy.


def full_match(possible_foods):
    known = {}
    while update_known(possible_foods, known):
        pass
    return known


def without_allergans(items):
    allergen_to_food = match_allergans(items)
    avoid = set(allergen_to_food.values())
    clean = set()
    for ingredients, _ in items:
        for k in ingredients:
            if k not in avoid:
                clean.add(k)
    return clean


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)  # 2960 is too high
    5
    """
    items = list(parse(text))
    clean = without_allergans(items)
    count = 0
    for ingredients, _ in items:
        for k in ingredients:
            if k in clean:
                count += 1
    return count


def part_2(text):
    """
    >>> part_2(EXAMPLE_TEXT)
    """
    items = list(parse(text))
    clean = without_allergans(items)
    allergen_to_food = match_allergans(items)
    food_to_allergen = {v: k for (k, v) in allergen_to_food.items()}
    dirty = set()
    for ingredients, _ in items:
        for k in ingredients:
            if k not in clean:
                dirty.add(k)
    return ",".join(sorted(dirty, key=lambda x: food_to_allergen[x]))


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
