function part_1(text)
    i = 0
    j = 0
    map = Set([(i, j)])
    for c in strip(text)
        if c == '>'
            j += 1
        elseif c == '<'
            j -= 1
        elseif c == 'v'
            i += 1
        elseif c == '^'
            i -= 1
        else
            error("unknown character $c")
        end
        if  !in((i, j), map)
            push!(map, (i, j))
        end
    end
    return length(map)
end

@assert part_1(">") == 2
@assert part_1("^>v<") == 4
@assert part_1("^v^v^v^v^v") == 2

function part_2(text)
    i = [0, 0]
    j = [0, 0]
    map = Set([(0, 0)])
    for (ndx, c) in enumerate(strip(text))
        if c == '>'
            j[ndx % 2 + 1] += 1
        elseif c == '<'
            j[ndx % 2 + 1] -= 1
        elseif c == 'v'
            i[ndx % 2 + 1] += 1
        elseif c == '^'
            i[ndx % 2 + 1] -= 1
        else
            error("unknown character $c")
        end
        if  !in((i[ndx % 2 + 1] , j[ndx % 2 + 1] ), map)
            push!(map, (i[ndx % 2 + 1] , j[ndx % 2 + 1] ))
        end
    end
    return length(map)
end

@assert part_2("^v") == 3
@assert part_2("^>v<") == 3
@assert part_2("^v^v^v^v^v") == 11

problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
