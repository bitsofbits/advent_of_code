
EXAMPLE_TEXT = """
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"""

function parse_line(line)
    line = strip(line[1: end-1])
    person, _, direction, amount, _, _, _, _, _, _, neighbor = split(line)
    amount = parse(Int, amount)
    if direction == "lose"
        amount = -amount
    else
        @assert direction == "gain"
    end
    return person, amount, neighbor
end

function parse_text(text)
    costs = Dict()
    for line in split(strip(text), "\n")
        person, amount, neighbor = parse_line(line)
        if !(haskey(costs, person))
            costs[person] = Dict()
        end
        costs[person][neighbor] = amount
    end
    return costs
end

function permutations(items)
    if length(items) == 1
        return items
    end
    perms = []
    for (i, x) in enumerate(items)
        others = [items[1:i - 1]; items[i + 1:end]]
        for y in permutations(others)
            push!(perms, [x ; y])
        end
    end
    return perms
end

function happiness(guests, costs)
    total = 0
    n = length(guests)
    @assert n == length(Set(guests))
    for (i, g) in enumerate(guests)
        last = guests[(i + n - 2) % n + 1]
        next = guests[i % n + 1]
        total += costs[g][last]
        total += costs[g][next]
    end
    return total
end

# 1144 is too high

function best_score(costs)
    guests = [x for x in keys(costs)]
    g0 = guests[1]
    best = typemin(Int)
    for others in permutations(guests[2:end])
        permuted = [[g0] ; others]
        best = max(best, happiness(permuted, costs))
    end
    return best
end

function part_1(text)
    costs = parse_text(text)
    return best_score(costs)
end

@assert part_1(EXAMPLE_TEXT) == 330

function part_2(text)
    costs = parse_text(text)
    guests = [x for x in keys(costs)]
    costs["ME"] = Dict()
    for g in guests
        costs[g]["ME"] = 0
        costs["ME"][g] = 0
    end
    return best_score(costs)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
