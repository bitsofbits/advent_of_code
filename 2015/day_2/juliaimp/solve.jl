
function process_line(line)
    (L, W, H) = map((x) -> parse(UInt128, x), split(strip(line), "x"))
    return 2 * (L*W + W*H + H * L)
end

function part_1(text)
    total = 0
    for line in split(problem_text, "\n")
        total += process_line(line)
    end
    return total
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")


