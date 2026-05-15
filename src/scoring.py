def calculate_path_cost(path, grid, terrain_cost):
    total = 0
    for row, col in path:

        terrain = grid[row][col]

        total += terrain_cost[terrain]
    return total

def grade_player(player_cost, optimal_cost):
    difference = player_cost - optimal_cost

    if difference == 0:
        return "S Rank"
    elif difference <= 2:
        return "A Rank"
    elif difference <= 5:
        return "B Rank"
    else:
        return "C Rank"