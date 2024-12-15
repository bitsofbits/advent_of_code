def render(board):
    max_i = max(i for (i, j) in board)
    max_j = max(j for (i, j) in board)
    rows = []
    for i in range(max_i + 1):
        row = []
        for j in range(max_j + 1):
            row.append(board.get((i, j), "."))
        rows.append("".join(row))
    return "\n".join(rows)


def parse(text, widen=False):
    """
    >>> location, board, moves = parse(EXAMPLE_TEXT)
    >>> location
    (4, 4)
    >>> moves[:12]
    '<vv>^<v^>v>^'
    >>> print(render(board))
    ##########
    #..O..O.O#
    #......O.#
    #.OO..O.O#
    #..O@..O.#
    #O#..O...#
    #O..O..O.#
    #.OO.O.OO#
    #....O...#
    ##########
    >>> _, wide_board, _ = parse(EXAMPLE_TEXT, widen=True)
    >>> print(render(wide_board))
    ####################
    ##....[]....[]..[]##
    ##............[]..##
    ##..[][]....[]..[]##
    ##....[]@.....[]..##
    ##[]##....[]......##
    ##[]....[]....[]..##
    ##..[][]..[]..[][]##
    ##........[]......##
    ####################
    """
    board_text, moves = text.strip().split("\n\n")
    board_text = board_text.strip()
    if widen:
        board_text = (
            board_text.replace("#", "##")
            .replace(".", "..")
            .replace("O", "[]")
            .replace("@", "@.")
        )
    moves = moves.strip().replace("\n", "")
    board = {}
    location = None
    for i, row in enumerate(board_text.strip().split("\n")):
        for j, x in enumerate(row):
            if x != ".":
                board[i, j] = x
            if x == "@":
                location = (i, j)
    return location, board, moves


unit_vectors = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def can_move_to(location, move, board):
    i, j = location
    di, dj = unit_vectors[move]
    target_location = (i + di, j + dj)
    if target_location in board:
        target_object = board[target_location]
        if target_object== "#":
            # Wall in the way, can't move
            return False
        can_move = can_move_to(target_location, move, board)
        if move in 'v^':
            if target_object == '[':
                offset_target_location = (i + di, j + dj + 1)
                can_move &= can_move_to(offset_target_location, move, board)
            if target_object == ']':
                offset_target_location = (i + di, j + dj - 1)
                can_move &= can_move_to(offset_target_location, move, board)
        if not can_move:
            # Can't move what's at target location
            return False
    return True

def apply_move_at(location, move, board):
    i, j = location
    di, dj = unit_vectors[move]
    target_location = (i + di, j + dj)
    if target_location in board:
        target_object = board[target_location]
        if target_object== "#":
            raise ValueError("can't move here")
        apply_move_at(target_location, move, board)
        if move in 'v^':
            if target_object == '[':
                offset_target_location = (i + di, j + dj + 1)
                apply_move_at(offset_target_location, move, board)
            if target_object == ']':
                offset_target_location = (i + di, j + dj - 1)
                apply_move_at(offset_target_location, move, board)
    board[target_location] = board.pop(location)
    return target_location


def part_1(text, widen=False, render_final=False):
    """
    >>> part_1(EXAMPLE_TEXT)
    10092
    >>> part_1(EXAMPLE_SMALL_TEXT)
    2028
    """
    location, board, moves = parse(text, widen)
    10092
    for x in moves:
        if can_move_to(location, x, board):
            location = apply_move_at(location, x, board)

    if render_final:
        print(render(board))

    score = 0
    for (i, j), v in board.items():
        if v in "O[":
            score += 100 * i + j
    return score


def part_2(text, render_final=False):
    """
    >>> part_2(EXAMPLE_TEXT, render_final=True)
    ####################
    ##[].......[].[][]##
    ##[]...........[].##
    ##[]........[][][]##
    ##[]......[]....[]##
    ##..##......[]....##
    ##..[]............##
    ##..@......[].[][]##
    ##......[][]..[]..##
    ####################
    9021
    """
    return part_1(text, widen=True, render_final=render_final)


if __name__ == "__main__":
    import doctest
    from pathlib import Path

    data_dir = Path(__file__).parents[1] / "data"
    with open(data_dir / "example.txt") as f:
        EXAMPLE_TEXT = f.read()
    with open(data_dir / "example_small.txt") as f:
        EXAMPLE_SMALL_TEXT = f.read()
    with open(data_dir / "example_2_small.txt") as f:
        EXAMPLE_2_SMALL_TEXT = f.read()
    doctest.testmod()
