from scoring import calculate_path_cost


class PlayerPath:
    def __init__(self, start):
        self.start = start
        self.path = [start]

    def reset(self):
        self.path = [self.start]

    @property
    def current_cell(self):
        return self.path[-1]

    def contains(self, cell):
        return cell in self.path

    def handle_cell_click(self, cell, terrain_map):
        if cell == self.current_cell:
            return False

        if len(self.path) >= 2 and cell == self.path[-2]:
            self.path.pop()
            return True

        if not terrain_map.is_passable(cell):
            return False
        if not self.is_adjacent(cell, self.current_cell):
            return False
        if cell in self.path:
            return False

        self.path.append(cell)
        return True

    def has_reached_end(self, end):
        return self.current_cell == end

    def cost(self, grid):
        return calculate_path_cost(self.path, grid)

    @staticmethod
    def is_adjacent(first, second):
        return abs(first[0] - second[0]) + abs(first[1] - second[1]) == 1
