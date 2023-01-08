using MD5


function find_suffix(text, n)
    i = 0
    prefix = repeat("0", n)
    while true
        hash = bytes2hex(md5(text * "$i"))
        if startswith(hash, prefix)
            return i
        end
        i += 1
    end
end

function part_1(text)
    return find_suffix(text, 5)
end

@assert part_1("abcdef") == 609043
@assert part_1("pqrstuv") == 1048970

function part_2(text)
    return find_suffix(text, 6)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
