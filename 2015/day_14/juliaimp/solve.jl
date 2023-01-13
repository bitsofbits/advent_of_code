EXAMPLE_TEXT = """
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
"""

struct Reindeer
    name::AbstractString
    speed::Int
    flight_duration::Int
    rest_duration::Int
end

function parse_line(line)
    line = strip(line)
    name, _, _, speed, _, _, fly, _, _, _, _, _, _, rest, _ = split(line)
    (speed, fly, rest) = (parse(Int, x) for x in (speed, fly, rest))
    return Reindeer(name, speed, fly, rest)
end

function parse_text(text)
    stable = Dict()
    for line in split(strip(text), "\n")
        x = parse_line(line)
        stable[x.name] = x
    end
    return stable
end

function simulate(stable, duration)
    pending = [(0, name, false, 0) for name in keys(stable)]
    points = Dict([name => 0 for name in keys(stable)])
    t = 0
    while t < duration
        next_pending = []
        for (t1, name, is_flying, distance) in pending
            rd = stable[name]
            if is_flying
                distance += rd.speed
            end
            if t1 == t
                if is_flying
                    next_t = t + rd.rest_duration
                else
                    next_t = t + rd.flight_duration
                end
                push!(next_pending,
                      (next_t, name, !is_flying, distance))
            else
                push!(next_pending, (t1, name, is_flying, distance))
            end
        end
        pending = next_pending
        if t >= 1
            best_score = maximum([x for (_, _, _, x) in pending])
            for (_, name, _, score) in pending
                if score == best_score
                    points[name] += 1
                end
            end
        end
        t += 1
    end
    return (maximum([x for (_, _, _, x) in pending]), 
            maximum(values(points)))
end

@assert simulate(parse_text(EXAMPLE_TEXT), 1000)  == (1120, 689)

function part_1(text)
    stable = parse_text(text)
    return simulate(stable, 2503)[1]
end

function part_2(text)
    stable = parse_text(text)
    return simulate(stable, 2503)[2]
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
