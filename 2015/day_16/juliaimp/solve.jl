ANALYSIS = """
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""

function parse_item(item)
    (name, value) = split(strip(item), ": ")
    return (name, parse(Int, value))
end

@assert parse_item("trees: 3") == ("trees", 3)

analysis = [parse_item(x) for x in split(strip(ANALYSIS), "\n")]
analysis = Dict([name => value for (name, value) in analysis])

function parse_text(text)
    aunts = Dict()
    for line in split(strip(text), "\n")
        (identifier, items) = split(strip(line), ": ", limit=2)
        _, number = split(strip(identifier))
        results = Dict()
        for chunk in split(items, ", ")
            (name, value) = parse_item(chunk)
            results[name] = value
        end
        aunts[number] = results
    end
    return aunts
end

function match(values)
    for (k, v) in values
        if k in keys(analysis) && analysis[k] != v
            return false
        end
    end
    return true
end

function part_1(text)
    aunts = parse_text(text)
    candidates = Set()
    for (id, values) in aunts
        if match(values)
            push!(candidates, id)
        end
    end
    (aunt,) = candidates
    return aunt
end

function match2(values)
    for (k, v) in values
        if k in keys(analysis)
            if k in ("cats", "trees")
                if analysis[k] >= v
                    return false
                end
            elseif k in ("pomeranians", "goldfish")
                if analysis[k] <= v
                    return false
                end
            else
                if analysis[k] != v
                    return false
                end
            end
        end
    end
    return true
end


function part_2(text)
    aunts = parse_text(text)
    candidates = Set()
    for (id, values) in aunts
        if match2(values)
            push!(candidates, id)
        end
    end
    (aunt,) = candidates
    return aunt
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
