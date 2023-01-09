
function parse_point(chunk)
    # Translate to 1 based indexing here
    return map((x) -> parse(Int, x) + 1, split(strip(chunk), ","))
end

function parse_line(line)
    line = strip(line)
    chunks = split(line)
    if length(chunks) == 5
        chunks = chunks[2:end]
    end
    cmd = chunks[1]
    p1 = parse_point(chunks[2])
    p2 = parse_point(chunks[4])
    return (cmd, p1, p2)
end


function part_1(text)
    lights = zeros(Bool, 1000, 1000)
    for line in split(strip(text), "\n")
        cmd, (x1, y1), (x2, y2) = parse_line(line)
        if cmd == "on"
            lights[x1:x2, y1:y2] .= true
        elseif cmd == "off"
            lights[x1:x2, y1:y2] .= false
        elseif cmd == "toggle"
            lights[x1:x2, y1:y2] = .!lights[x1:x2, y1:y2]
        else
            error("unexpected command: $cmd")
        end
    end
    count = 0
    for i in 1:1000
        for j in 1:1000
            if lights[i, j]
                count += 1
            end
        end
    end
    return count
end

function part_2(text)
    lights = zeros(Int, 1000, 1000)
    for line in split(strip(text), "\n")
        cmd, (x1, y1), (x2, y2) = parse_line(line)
        if cmd == "on"
            lights[x1:x2, y1:y2] = lights[x1:x2, y1:y2] .+ 1
        elseif cmd == "off"
            mask = lights[x1:x2, y1:y2] .> 0
            lights[x1:x2, y1:y2] = lights[x1:x2, y1:y2] - (1 .* mask)
        elseif cmd == "toggle"
            lights[x1:x2, y1:y2] = lights[x1:x2, y1:y2] .+ 2
        else
            error("unexpected command: $cmd")
        end
    end
    count = 0
    for i in 1:1000
        for j in 1:1000
            count += lights[i, j]
        end
    end
    return count
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
