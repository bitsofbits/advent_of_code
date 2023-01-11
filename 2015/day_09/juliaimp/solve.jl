EXAMPLE_TEXT = """
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"""

function parse_line(line)
    (origin, _, dest, _, cost) = split(strip(line))
    return (origin, dest, parse(Int, cost))
end

function parse_text(text)
    routes = Dict()
    for line in split(strip(text), "\n")
        origin, dest, cost = parse_line(line)
        if !(origin in keys(routes))
            routes[origin] = Dict()
        end
        routes[origin][dest] = cost
        if !(dest in keys(routes))
            routes[dest] = Dict()
        end
        routes[dest][origin] = cost
    end
    return routes
end

function compute_historic_cost(history, routes)
    origin = history[1]
    total = 0
    for dest in history[2:end]
        total += routes[origin][dest]
        origin = dest
    end
    return total
end

function find_fastest(routes)
    all_nodes = Set([k for k in keys(routes)])
    lowest_cost = typemax(Int)
    best_history = []
    states = Dict((k, Set([])) => 0 for k in all_nodes)
    stack = [(k, 0, Set([k]), [k]) for k in all_nodes]
    while !isempty(stack)
        origin, cost, visited, history = pop!(stack)
        if visited == all_nodes
            if cost < lowest_cost
                lowest_cost = cost
                best_history = history
            end
        end
        for (dest, route_cost) in routes[origin]
            if dest in visited
                # Can only visit each location once
                continue
            end
            next_cost = cost + route_cost
            key = (dest, visited)
            if next_cost < get(states, key, typemax(Int))
                states[key] = next_cost
                next_visited = union(visited, Set([dest]))
                next_history = [history ; [dest]]
                push!(stack, (dest, next_cost, next_visited, next_history))
            end
        end
    end
    @assert length(best_history) == length(all_nodes)
    @assert compute_historic_cost(best_history, routes) == lowest_cost
    return (lowest_cost, best_history)
end

@assert find_fastest(parse_text(EXAMPLE_TEXT))[1] == 605


function part_1(text)
    return find_fastest(parse_text(text))[1]
end

function find_slowest(routes) 
    all_nodes = Set([k for k in keys(routes)])
    highest_cost = 0
    best_history = []
    states = Dict((k, Set([])) => 0 for k in all_nodes)
    stack = [(k, 0, Set([k]), [k]) for k in all_nodes]
    while !isempty(stack)
        origin, cost, visited, history = pop!(stack)
        if visited == all_nodes
            if cost > highest_cost
                highest_cost = cost
                best_history = history
            end
        end
        for (dest, route_cost) in routes[origin]
            if dest in visited
                # Can only visit each location once
                continue
            end
            next_cost = cost + route_cost
            key = (dest, visited)
            if next_cost > get(states, key, 0)
                states[key] = next_cost
                next_visited = union(visited, Set([dest]))
                next_history = [history ; [dest]]
                push!(stack, (dest, next_cost, next_visited, next_history))
            end
        end
    end
    @assert length(best_history) == length(all_nodes)
    @assert compute_historic_cost(best_history, routes) == highest_cost
    return (highest_cost, best_history)
end

function part_2(text)
    return find_slowest(parse_text(text))[1]
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
