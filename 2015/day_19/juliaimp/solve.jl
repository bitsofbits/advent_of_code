
function parse_line(line)
    return split(strip(line), " => ")
end

function parse_text(text)
    (repltext, molecule) = split(strip(text), "\n\n")
    molecule = strip(molecule)
    replacements = Dict()
    for line in split(strip(repltext), "\n")
        line = strip(line)
        k, v = parse_line(line)
        if !(haskey(replacements, k))
            replacements[k] = []
        end
        push!(replacements[k], v)
    end
    return molecule, replacements
end


function create(molecule, replacements)
    created = Set()
    for i in 1:length(molecule)
        for (k, values) in replacements
            d = length(k) - 1
            if i + d <= length(molecule)
                if molecule[i:i + d] == k
                    for r in values
                        push!(created, molecule[1:i-1] * r * molecule[i + d + 1:end])
                    end
                end
            end
        end
    end
    return created
end

function part_1(text)
    return length(create(molecule, replacements))
end

function unsynthesize(revrep, target)
    pending = [(target, 0)]
    max_repl = maximum([length(x) for x in keys(revrep)])
    while length(pending) > 0
        m, cnt = pop!(pending)
        if m == "e"
            # Not entirely happy with this; wanted to do a general
            # solution, but I'm just assuming a greedy solution works here.
            return cnt
        end
        for i in 1:length(m)
            for d in 0:(max_repl - 1)
                if i + d > length(m)
                    continue
                end
                k = m[i:i+d]
                if haskey(revrep, k)
                    r = revrep[k]
                    m1 = join([m[1:i - 1], r, m[i + d + 1:end]], "")
                    if (r == "e") && (m1 != "e")
                        continue
                    end
                    push!(pending, (m1, cnt + 1))
                end
            end
        end
    end
    return cnt
end


function part_2(text)
    return unsynthesize(reversed, molecule)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

molecule, replacements = parse_text(problem_text)


reversed = Dict()
for (k, list) in replacements
    for v in list
        @assert !haskey(reversed, v)
        reversed[v] = k
    end
end


pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
