import random

from dijkstra import compute_dijkstra
from settings import HABITAT_START_TERRAIN, HABITAT_TERRAIN_WEIGHTS, TERRAIN_COSTS


class TerrainMap:
    def __init__(self, grid_size, habitat):
        self.grid_size = grid_size
        self.habitat = habitat
        self.start = (0, 0)
        self.end = (grid_size - 1, grid_size - 1)
        self.grid = []
        self.generate_reachable_map()

    def generate_reachable_map(self):
        for _ in range(500):
            self.grid = self.create_random_grid()
            path, cost = compute_dijkstra(self.grid, self.start, self.end)
            if path and cost < float("inf"):
                return

        base = HABITAT_START_TERRAIN[self.habitat]
        self.grid = [[base for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def create_random_grid(self):
        choices = HABITAT_TERRAIN_WEIGHTS[self.habitat]
        names = list(choices.keys())
        weights = list(choices.values())
        grid = []

        for _ in range(self.grid_size):
            grid.append(random.choices(names, weights=weights, k=self.grid_size))

        safe_tile = HABITAT_START_TERRAIN[self.habitat]
        grid[self.start[0]][self.start[1]] = safe_tile
        grid[self.end[0]][self.end[1]] = safe_tile
        return grid

    def is_passable(self, cell):
        row, col = cell
        if not (0 <= row < self.grid_size and 0 <= col < self.grid_size):
            return False
        return TERRAIN_COSTS[self.grid[row][col]] is not None

    def terrain_at(self, cell):
        row, col = cell
        return self.grid[row][col]
