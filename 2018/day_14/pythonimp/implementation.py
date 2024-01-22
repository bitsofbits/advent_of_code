def parse(text):
    return int(text.strip())


def step(recipes, indices):
    recipe_sum = sum(recipes[i] for i in indices)
    new_recipes = [int(x) for x in str(recipe_sum)]
    recipes.extend(new_recipes)
    new_indices = [(i + 1 + recipes[i]) % len(recipes) for i in indices]
    return recipes, new_indices


def part_1(text):
    """
    >>> part_1(EXAMPLE_TEXT)
    '5158916779'
    """
    steps = parse(text)
    recipes = [3, 7]
    indices = [0, 1]
    while len(recipes) < steps + 10:
        recipes, indices = step(recipes, indices)
    return ''.join(str(x) for x in recipes[steps : steps + 10])


def part_2(text):
    """
    >>> part_2("92510")
    18

    20283721
    """
    pattern = [int(x) for x in text.strip()]
    n = len(pattern)
    recipes = [3, 7]
    indices = [0, 1]
    while True:
        recipes, indices = step(recipes, indices)
        if recipes[-n:] == pattern:
            return len(recipes) - n
        if recipes[-(n + 1) : -1] == pattern:
            return len(recipes) - n - 1


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()

    doctest.testmod()
