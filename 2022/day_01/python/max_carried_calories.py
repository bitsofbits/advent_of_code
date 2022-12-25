def compute_max_carried_calories(path):
    max_calories = 0
    calories = 0
    for line in open(path):
        if line.strip():
            calories += float(line)
        else:
            max_calories = max(max_calories, calories)
            calories = 0
    return max_calories


def top_three_elves_calories(path):
    calorie_list = []
    calories = 0
    for line in open(path):
        if line.strip():
            calories += float(line)
        else:
            calorie_list.append(calories)
            calories = 0
    top_three = sorted(calorie_list)[-3:]
    return sum(top_three)


print(top_three_elves_calories("data/calories.txt"))
