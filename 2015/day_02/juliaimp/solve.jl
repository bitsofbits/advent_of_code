
function process_line_pt1(line)
    (L, W, H) = map((x) -> parse(Int, x), split(strip(line), "x"))
    faces = [L * W, W * H, H * L]

    return 2 * sum(faces) + minimum(faces)
end

@assert process_line_pt1("2x3x4") == 58
@assert process_line_pt1("1x1x10") == 43

function part_1(text)
    total = 0
    for line in split(problem_text, "\n")
        total += process_line_pt1(line)
    end
    return total
end


function process_line_pt2(line)
    (L, W, H) = map((x) -> parse(Int, x), split(strip(line), "x"))
    half_perimeters = [L + W, W + H, H + L]
    volume = L * W * H
    return 2 * minimum(half_perimeters) + volume
end


@assert process_line_pt2("2x3x4") == 34
@assert process_line_pt2("1x1x10") == 14


function part_2(text)
    total = 0
    for line in split(problem_text, "\n")
        total += process_line_pt2(line)
    end
    return total
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
