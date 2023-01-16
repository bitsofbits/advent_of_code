
function parse_text(text)
    values = []
    for line in split(strip(text))
        push!(values, parse(Int, strip(line)))
    end
    return values
end


function subsets(items, used, total, target)
    if length(items) == 1
        return items
    end
    perms = []
    for (i, x) in enumerate(items)
        if i in used
            continue
        end

        next_total = total + x
        if next_total > target
            continue
        elseif next_total == target
            push!(perms, x)
        else
            next_used = copy(used)
            push!(used, i)
            others = [items[1:i - 1]; items[i + 1:end]]
            for y in subsets(others, next_used, next_total, target)
                push!(perms, [x ; y])
            end
        end
    end
    return perms
end


function part_1(text)
    sizes = parse_text(text)
    return length(subsets(sizes, Set(), 0, 150))
end

function part_2(text)
    sizes = parse_text(text)
    s = subsets(sizes, Set(), 0, 150)
    n = minimum([length(x) for x in s])
    return length([x for x in s if length(x) == n])
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
