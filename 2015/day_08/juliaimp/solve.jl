

function count_extra_chars(line)
    cnt = 2
    line = strip(line)
    @assert line[1] == '"' && line[end] == '"'
    i = 2
    while i < length(line)
        last = line[i - 1]
        c = line[i]
        if last == '\\'
            if c == 'x'
                cnt += 3
                i += 3
            else
                @assert c in ('\\', '\"')
                cnt += 1
                i += 1
            end
        end
        i += 1
    end
    return cnt
end

@assert count_extra_chars("\"\"") == 2
@assert count_extra_chars("\"abc\"") == 2
@assert count_extra_chars("\"aaa\\\"aaa\"") == 3
@assert count_extra_chars("\"\\x27\"") == 5


function part_1(text)
    return sum(map(count_extra_chars, split(text, "\n")))
end

function count_extra_chars_2(line)
    cnt = 4
    line = strip(line)
    @assert line[1] == '"' && line[end] == '"'
    i = 2
    while i < length(line)
        c = line[i]
        if c  in ('\\', '"')
            cnt += 1
        end
        i += 1
    end
    return cnt
end

function part_2(text)
    return sum(map(count_extra_chars_2, split(text, "\n")))
end

@assert count_extra_chars_2("\"\"") == 4
@assert count_extra_chars_2("\"abc\"") == 4
@assert count_extra_chars_2("\"aaa\\\"aaa\"") == 6
@assert count_extra_chars_2("\"\\x27\"") == 5


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
