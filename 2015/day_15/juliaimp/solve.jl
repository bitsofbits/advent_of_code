EXAMPLE_TEXT = """
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
"""


function parse_line(line)
    line = strip(line)
    name, rest = split(line, ":")
    rest = strip(rest)
    itemstrs = split(rest, ",")
    props = Dict()
    for txt in itemstrs
        txt = strip(txt)
        key, amt = split(txt)
        amt = parse(Int, amt)
        props[key] = amt
    end
    return name, props
end

function parse_text(text)
    text = strip(text)
    ingredients = Dict()
    for line in split(text, "\n")
        k, v = parse_line(line)
        ingredients[k] = v
    end
    return ingredients
end


function score(amounts, ingredients)
    counts = Dict()
    for (name, n) in amounts
        for (prop, score) in ingredients[name]
            if !(prop in keys(counts))
                counts[prop] = 0
            end
            counts[prop] += n * score
        end
    end
    return prod([max(v, 0) for (k, v) in counts if k != "calories"])
end

function calories(amounts, ingredients)
    cals = 0
    for (name, n) in amounts
        cals += n * ingredients[name]["calories"]
    end
    return cals
end


function solve(ingredients, calory_cnt)
    names = [x for x in keys(ingredients)]
    remaining = 100
    best_score = 0
    best_amounts = Dict()
    n = length(names)
    for i in 0:(100 ^ (n - 1))
        amounts = []
        for _ in 1:n - 1
            push!(amounts, i % 100)
            i = Int(floor(i / 100))
        end
        tot = sum(amounts)
        if tot > 100
            continue
        end
        push!(amounts, 100 - tot)
        amt_dict = Dict(k => v for (k, v) in zip(names, amounts))
        if calory_cnt == 0 || calories(amt_dict, ingredients) == calory_cnt
            @assert sum(values(amt_dict)) == 100
            scr = score(amt_dict, ingredients)
            if scr > best_score
                best_score = scr
                best_amounts = amt_dict
            end
        end
    end
    return best_score
end



@assert score(Dict("Butterscotch" => 44, "Cinnamon" => 56), 
    parse_text(EXAMPLE_TEXT)) == 62842880

@assert solve(parse_text(EXAMPLE_TEXT), 0) == 62842880

@assert solve(parse_text(EXAMPLE_TEXT), 500) == 57600000


function part_1(text)
    ingredients = parse_text(text)
    return solve(ingredients, 0)
end

function part_2(text)
    ingredients = parse_text(text)
    return solve(ingredients, 500)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
