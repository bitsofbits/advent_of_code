
function count_vowels(line)
    cnt = 0
    for c in line
        if c in "aeiou"
            cnt += 1
        end
    end
    return cnt
end

function count_double_letters(line)
    cnt = 0
    last = line[1]
    for c in line[2:end]
        if c == last
            cnt += 1
        end
        last = c
    end
    return cnt
end

function has_bad_pairs(line)
    bad = Set([('a', 'b'), ('c', 'd'), ('p', 'q'), ('x', 'y')])
    last = line[1]
    for c in line[2:end]
        if (last, c) in bad
            return true
        end
        last = c
    end
    return false
end


function is_nice1(line)
    nice = (
        (count_vowels(line) >= 3)
      && (count_double_letters(line) > 0)
      && !has_bad_pairs(line)
          )  
    return nice
end


function has_repeated_pair(line)
    pairs = Set()
    last = line[1]
    skip = 0
    for c in line[2:end]
        if (skip <= 0) || (c != last)
            if in((last, c), pairs)
                return true
            else
                push!(pairs, (last, c))
                if c == last
                    skip = 2
                end
            end
        end
        skip -= 1
        last = c
    end
    return false

end

function count_sandwiches(line)
    cnt = 0
    last2 = line[1]
    last1 = line[2]
    for c in line[3:end]
        if (c == last2)
            cnt += 1
        end
        last2 = last1
        last1 = c
    end
    return cnt
end

function is_nice2(line)
    nice = (
        has_repeated_pair(line)   # wrong
      & (count_sandwiches(line) > 0)
          )  
    return nice
end

@assert is_nice2("qjhvhtzxzqqjkmpb") == true
@assert is_nice2("xxyxx") == true
@assert is_nice2("uurcxstgmygtbstg") == false
@assert is_nice2("ieodomkazucvgmuy") == false
@assert is_nice2("aaabcb") == false




function part_1(text)
    return length(filter(is_nice1, split(strip(text), "\n")))
end

function part_2(text)
    return length(filter(is_nice2, split(strip(text), "\n")))
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
