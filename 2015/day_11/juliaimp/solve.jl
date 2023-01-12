function to_ints(text)
    ints = []
    for c in text
        push!(ints, c - 'a')
    end
    return ints
end

@assert to_ints("abcxyz") == [0, 1, 2, 23, 24, 25]

function from_ints(ints)
    chars = []
    for n in ints
        push!(chars, 'a' + n)
    end
    return join(chars, "")
end

@assert from_ints([0, 1, 2, 23, 24, 25]) == "abcxyz"

function next_password(ints)
    c = 1
    next = []
    for n in reverse(ints)
        n = n + c
        c = div(n, 26)
        push!(next, n % 26)
    end
    if c > 0
        return [0 for _ in ints]
    end
    return reverse(next)
end

@assert from_ints(next_password(to_ints("abcxyz"))) == "abcxza"

function has_straight(ints)
    i = 3
    while i <= length(ints)
        if (ints[i] == ints[i - 1] + 1) && (ints[i - 1] == ints[i - 2] + 1)
            return true
        end
        i += 1
    end
    return false
end

@assert !has_straight("hxbxxaaa")


function no_iol(ints)
    bad = Set([c - 'a' for c in "iol"])
    for x in ints
        if x in bad
            return false
        end
    end
    return true
end

function n_pairs(ints)
    pairs = Set()
    i = 2
    while i <= length(ints)
        if ints[i - 1] == ints[i]
            push!(pairs, i)
            i += 1
        end
        i += 1
    end
    return length(pairs)
end

@assert n_pairs(to_ints("abbceffg")) == 2

function is_valid(ints)
    return has_straight(ints) &&
           no_iol(ints) &&
           (n_pairs(ints) >= 2) 
end


@assert !is_valid(to_ints("hijklmmn"))
@assert !is_valid(to_ints("abbceffg"))
@assert !is_valid(to_ints("aabcegjk"))

function part_1(text)
    ints = next_password(to_ints(text))
    while !is_valid(ints)
        ints = next_password(ints)
    end
    return from_ints(ints)
end

function part_2(text)
    return part_1(part_1(text))
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
