EXAMPLE_TEXT = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

EXAMPLE1_TEXT = """
..##..
..##.#
...##.
......
#.....
#.##..
"""


function parse_text(text)
    text = strip(text)
    board = Set()
    for (i, line) in enumerate(split(text, "\n"))
        for (j, c) in enumerate(line)
            if c == '#'
                push!(board, (i, j))
            end
        end
    end
    return board
end

@assert length(parse_text(EXAMPLE_TEXT)) == 15

function advance!(board, size, stuck)
    neighbors = Dict()
    for k in stuck
        push!(board, k)
    end
    for (i0, j0) in board
        for di in [-1, 0, 1]
            for dj in [-1, 0, 1]
                key = (i0 + di, j0 + dj)
                if !haskey(neighbors, key)
                    neighbors[key] = 0
                end
                if !(di == 0 && dj == 0)
                    neighbors[key] += 1
                end
            end
        end
    end
    for (k, n) in neighbors
        if k in board
            if !(n in (2, 3))
                pop!(board, k)
            end
        else
            (i, j) = k
            if n == 3 && i > 0 && i <= size && j > 0 && j <= size
                push!(board, k)
            end
        end
    end
    for k in stuck
        push!(board, k)
    end
end

example_board = parse_text(EXAMPLE_TEXT)
advance!(example_board, 6, Set())
@assert example_board  == parse_text(EXAMPLE1_TEXT)

function part_1(text)
    board = parse_text(text)
    for _ in 1:100
        advance!(board, 100, Set())
    end
    return length(board)
end

function part_2(text)
    board = parse_text(text)
    stuck = Set([(1, 1), (100, 1), (1, 100), (100, 100)])
    for _ in 1:100
        advance!(board, 100, stuck)
    end
    return length(board)
end


problem_text = open(ARGS[1],"r") do f
    strip(read(f, String))
end

pt1 = part_1(problem_text)
println("part_1: $pt1")

pt2 = part_2(problem_text)
println("part_2: $pt2")
