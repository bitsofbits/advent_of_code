
function split_into_runs(text)
    i0 = 1
    chunks = []
    for (i1, c) in enumerate(text)
        if c != text[i0]
            push!(chunks, text[i0:i1-1])
            i0 = i1
        end
    end
    if length(text) >= i0
        push!(chunks, text[i0:end])
    end
    return chunks
end


function look_and_say(text)
    text = strip(text)
    chunks = []
    for r in split_into_runs(text)
        cnt = length(r)
        push!(chunks, "$cnt")
        push!(chunks, r[1:1])
    end
    return join(chunks, "")
end

@assert look_and_say("1211") == "111221"
@assert look_and_say("111221") == "312211"

function part_1(text)
    for _ in 1:40
        text = look_and_say(text)
    end
    return length(text)
end

function part_2(text)
    for _ in 1:50
        text = look_and_say(text)
    end
    return length(text)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
