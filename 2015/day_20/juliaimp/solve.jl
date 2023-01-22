




function sieve1(x)
    scores = zeros(Int, x)
    for i in 1:x
        scores[i:i:x] .+= 10 * i
        if scores[i] >= x
            return i
        end
    end
end

@assert sieve1(130) == 8

function part_1(text)
    return sieve1(target)
end


function sieve2(x)
    scores = zeros(Int, x)
    for i in 1:x
        lst = min(x, 50 * i)
        scores[i:i:lst] .+= 11 * i
        if scores[i] >= x
            return i
        end
    end
end


function part_2(text)
    return sieve2(target)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end
target = parse(Int, problem_text)


pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
