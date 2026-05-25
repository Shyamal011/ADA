def is_adjacent(current, next_cell):

    r1, c1 = current
    r2, c2 = next_cell

    return abs(r1 - r2) + abs(c1 - c2) == 1


def add_to_path(path, clicked_cell, grid):

    terrain = grid[clicked_cell[0]][clicked_cell[1]]

    if terrain == "water":
        return path

    if len(path) == 0:
        path.append(clicked_cell)
        return path

    last_cell = path[-1]

    if is_adjacent(last_cell, clicked_cell):

        if clicked_cell not in path:
            path.append(clicked_cell)

    return path