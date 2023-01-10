
function try_int(chars)
    try
        return parse(UInt16, chars)
    catch _
        return chars
    end
end


function parse_line(line)
    line = strip(line)
    src, dest = split(line, " -> ")
    parts = split(src)
    if length(parts) == 1
        cmd = "SET"
        args = parts
    elseif length(parts) == 2
        (cmd, arg) = parts
        args = [arg]
    elseif length(parts) == 3
        (arg1, cmd, arg2) = parts
        args = [arg1, arg2]
    else
        error("malformed command: $line")
    end
    args = map(try_int, args)
    return cmd, args, dest
end

# println(parse_line("x AND 5 -> d"))

EXAMPLE_TEXT = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

function parse_text(text)
    circuit = Dict()
    for (cmd, args, dest) in map(parse_line, split(strip(text), "\n"))
        circuit[dest] = (cmd, args)
    end
    return circuit
end

# @show parse_text(EXAMPLE_TEXT)

function eval(circuit, wire :: UInt16)
    return wire
end

function eval(circuit, wire)
    if circuit[wire] isa UInt16
        return circuit[wire]
    end
    cmd, args = circuit[wire]
    if cmd == "SET"
        (x,) = args
        circuit[wire] = eval(circuit, x)
    elseif cmd == "NOT"
        (x,) = args
        circuit[wire] =  ~eval(circuit, x)
    elseif cmd == "AND"
        (x, y) = args
        circuit[wire] =  eval(circuit, x) &  eval(circuit, y)
    elseif cmd == "OR"
        (x, y) = args
        circuit[wire] =  eval(circuit, x) | eval(circuit, y)
    elseif cmd == "LSHIFT"
        (x, y) = args
        circuit[wire] =  eval(circuit, x) << eval(circuit, y) 
    elseif cmd == "RSHIFT"
        (x, y) = args
        circuit[wire] =  eval(circuit, x) >>> eval(circuit, y)   
    else
        error("unknown command $cmd")
    end
    return circuit[wire]
end



function part_1(text)
    circuit = parse_text(text)
    return eval(circuit, "a")
end

function part_2(text)
    circuit = parse_text(text)
    circuit["b"] = UInt16(46065)
    return eval(circuit, "a")
end


@assert eval(parse_text(EXAMPLE_TEXT), "i") == 65079

problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)  # -> 1440710 is too low!
println("part_1: $pt1")

pt2 = part_2(problem_text)  # -> 1440710 is too low!
println("part_2: $pt2")
