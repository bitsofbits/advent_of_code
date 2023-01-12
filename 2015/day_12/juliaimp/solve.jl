# import Pkg; Pkg.add("JSON")
import JSON

function parse(text)
    return JSON.parse(text)
end

function find_numbers!(numbers, obj :: String)
end

function find_numbers!(numbers, obj :: Int)
    push!(numbers, obj)
end

function find_numbers!(numbers, obj :: Dict)
    for (k, v) in obj
        find_numbers!(numbers, k)
        find_numbers!(numbers, v)
    end
end

function find_numbers!(numbers, obj :: Array)
    for x in obj
        find_numbers!(numbers, x)
    end
end


function part_1(text)
    obj = parse(text)
    numbers = []
    find_numbers!(numbers, obj)
    return sum(numbers)
end

function find_numbers2!(numbers, obj :: String)
end

function find_numbers2!(numbers, obj :: Int)
    push!(numbers, obj)
end

function find_numbers2!(numbers, obj :: Dict)
    if !("red" in values(obj))
        for (k, v) in obj
            find_numbers2!(numbers, k)
            find_numbers2!(numbers, v)
        end
    end
end

function find_numbers2!(numbers, obj :: Array)
    for x in obj
        find_numbers2!(numbers, x)
    end
end

function part_2(text)
    obj = parse(text)
    numbers = []
    find_numbers2!(numbers, obj)
    return sum(numbers)
end

problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
