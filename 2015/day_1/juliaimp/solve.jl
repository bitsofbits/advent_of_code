
problem_text = open("data/input.txt","r") do f
    read(f, String)
end

function part_1(text)
    floor = 0
    for c in strip(text)
        if c == '('
            floor += 1
        elseif c == ')'
            floor -= 1
        else
            error("unknown character: $c")
        end
    end
    return  floor
end

function part_2(text)
    floor = 0
    step = 0
    for (i, c) in enumerate(strip(text))
        if c == '('
            floor += 1
        elseif c == ')'
            floor -= 1
        else
            error("unknown character: $c")
        end
        if floor == -1
            step = i
            break
        end
    end
    return  step
end

p1 = part_1(problem_text)
println("part_1 = $p1")

p2 = part_2(problem_text)
println("part_2 = $p2")