from settings import RANK_COLORS, TERRAIN_COSTS


def calculate_path_cost(path, grid):
    total = 0
    for row, col in path[1:]:
        cost = TERRAIN_COSTS[grid[row][col]]
        if cost is None:
            return float("inf")
        total += cost
    return total


def get_grade(player_cost, optimal_cost):
    diff = player_cost - optimal_cost
    if diff == 0:
        return "S Rank"
    if diff <= 2:
        return "A Rank"
    if diff <= 5:
        return "B Rank"
    return "C Rank"


def is_victory(player_cost, optimal_cost):
    return player_cost == optimal_cost


def grade_color(grade):
    return RANK_COLORS.get(grade, RANK_COLORS["C Rank"])
