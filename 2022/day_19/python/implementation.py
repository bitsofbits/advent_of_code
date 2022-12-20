from concurrent.futures import ProcessPoolExecutor


def parse_blueprint(line):
    lblstr, coststr = line.split(":")
    *_, lblstr = lblstr.strip().split()
    lbl = int(lblstr)
    all_costs = {}
    for txt in coststr.split("."):
        txt = txt.strip()
        if not txt:
            continue
        tokens = txt.split()
        assert tokens[0] == "Each", tokens
        kind = tokens[1]
        all_costs[kind] = costs = {}
        assert tokens[2:4] == ["robot", "costs"]
        tokens = tokens[4:]
        for i in range(0, len(tokens), 3):
            costs[tokens[i + 1]] = int(tokens[i])
    return lbl, all_costs


def load_blueprints(path):
    """
    >>> blueprints = load_blueprints("data/example.txt")
    >>> list(blueprints.keys())
    [1, 2]
    >>> for k, v in blueprints.items(): print(v)
    {'ore': {'ore': 4}, 'clay': {'ore': 2}, 'obsidian': {'ore': 3, 'clay': 14}, 'geode': {'ore': 2, 'obsidian': 7}}
    {'ore': {'ore': 2}, 'clay': {'ore': 3}, 'obsidian': {'ore': 3, 'clay': 8}, 'geode': {'ore': 3, 'obsidian': 12}}
    """
    blueprints = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                k, v = parse_blueprint(line)
                blueprints[k] = v
    return blueprints


def upper_bound(t, costs, robots, ore):
    """Estimate upper bound for score based on current state.

    Whenever the real rules require us to make a choice such as
    which robot to build or whether to use a resource for building
    one robot or another, we do both. So:

    * We can build as many robots per time step as we want
    * Nothing requires ore

    With these two constraints we can quickly determine a bound. We could
    go further and include the dependency of clay robots on ore, but it
    adds some complexity since we are removing the clay cost below and it
    doesn't actually help.

    """
    OG = ore["geode"]
    OO = ore["obsidian"]
    OC = ore["clay"]
    RG = robots["geode"]
    RO = robots["obsidian"]
    RC = robots["clay"]
    CGO = costs["geode"]["obsidian"]
    COC = costs["obsidian"]["clay"]
    while t > 0:
        OG += RG
        if OO >= CGO:
            OO -= CGO
            RG += 1
        OO += RO
        if OC >= COC:
            RO += 1
            OC -= COC
        OC += RC
        RC += 1
        t -= 1
    return OG


class Factory:
    """
    >>> blueprints = load_blueprints("data/example.txt")
    >>> factory = Factory(blueprints[1])
    >>> factory.find_max_geodes(24)
    9
    >>> factory.find_max_geodes(32)
    56
    >>> factory = Factory(blueprints[2])
    >>> factory.find_max_geodes(24)
    12
    >>> factory.find_max_geodes(32)
    62
    """

    initial_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}

    def __init__(self, costs):
        self.costs = costs
        self.best_score = 0
        self.states = {}
        self.max_ore_costs = max(x["ore"] for x in self.costs.values())

    def find_max_geodes(self, time):
        robots = self.initial_robots.copy()
        ore = {k: 0 for k in robots.keys()}
        return self._fmg(time, self.costs, robots, ore)

    def _fmg(self, time_left, costs, robots, ore):
        if time_left == 2:
            # No matter what, we get this much
            geodes = ore["geode"] + 2 * robots["geode"]
            if all(v <= ore[k] for (k, v) in costs["geode"].items()):
                # If possible we build one more geode robot to get one more geode
                geodes += 1
            return geodes

        if "ore" in costs and robots["ore"] == self.max_ore_costs:
            # Remove ore from costs so we don't build ore robots any more
            costs = {k: v for (k, v) in costs.items() if k != "ore"}
        if "clay" in costs and robots["clay"] == costs["obsidian"]["clay"]:
            # Remove clay from costs so we don't build clay robots any more
            costs = {k: v for (k, v) in costs.items() if k != "clay"}
        if robots["obsidian"] == costs["geode"]["obsidian"]:
            if robots["ore"] >= costs["geode"]["ore"]:
                # We build geode robots every time, so do that
                return ore["geode"] + time_left * (robots["geode"] + time_left - 1) // 2
            else:
                # Remove obsidian from costs so we don't build any more.
                costs = {k: v for (k, v) in costs.items() if k != "obsidian"}

        # If our score is less than our estimated upper bound give up on this path.
        local_best_score = upper_bound(time_left, costs, robots, ore)
        if local_best_score < self.best_score:
            return -1

        # Make a key based on the current state
        key = (time_left, frozenset(robots.items()), frozenset(ore.items()))
        if key in self.states:
            # We've seen this state before, so just return it's value
            return self.states[key]

        time_left -= 1

        # Later on, we check if we can build a robot are based on the current
        # ore so make a copy and update that based on the count of each robot.
        updated_ore = ore.copy()
        for k, cnt in robots.items():
            updated_ore[k] += cnt

        # Try not building anything
        geodes = self._fmg(time_left, costs, robots, updated_ore)
        # Try building a robot
        for robot_type, robot_costs in costs.items():
            if all(v <= ore[k] for (k, v) in robot_costs.items()):
                # We can build this type of robot, so let's try
                # We need to copy any objects we are going to modify
                # so we don't mess them up for other paths.
                local_ore = updated_ore.copy()
                for k, v in robot_costs.items():
                    local_ore[k] -= v
                local_robots = robots.copy()
                local_robots[robot_type] += 1
                geodes = max(
                    geodes,
                    self._fmg(
                        time_left,
                        costs,
                        local_robots,
                        local_ore,
                    ),
                )

        # Store this state in case we see it again
        self.states[key] = geodes
        # Update the best score, so we can use it with upper_bound (above)
        self.best_score = max(self.best_score, geodes)
        return geodes


def find_max_geodes_24(blueprint):
    return Factory(blueprint).find_max_geodes(24)


def compute_total_quality(blueprints):
    total_quality = 0
    keys = list(blueprints)
    args = [blueprints[k] for k in keys]
    with ProcessPoolExecutor() as exe:
        for k, g in zip(keys, exe.map(find_max_geodes_24, args)):
            q = k * g
            print(k, g, q)
            total_quality += q
    return total_quality


def find_max_geodes_32(blueprint):
    return Factory(blueprint).find_max_geodes(32)


def compute_geode_product(blueprints):
    prod = 1
    keys = list(blueprints.keys())[:3]
    assert keys == [1, 2, 3][: len(keys)], keys
    args = [blueprints[k] for k in keys]
    with ProcessPoolExecutor() as exe:
        for k, g in zip(keys, exe.map(find_max_geodes_32, args)):
            print(k, g)
            prod *= g
    return prod


if __name__ == "__main__":
    import doctest

    doctest.testmod()
