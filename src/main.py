import pygame

from dijkstra import compute_dijkstra
from player import PlayerPath
from scoring import get_grade, grade_color, is_victory
from settings import (
    BUTTON_HEIGHT,
    COLOR_ACCENT,
    COLOR_BG,
    COLOR_BG_2,
    COLOR_END,
    COLOR_GRID_LINE,
    COLOR_HOVER,
    COLOR_MUTED,
    COLOR_OPTIMAL,
    COLOR_OPTIMAL_GLOW,
    COLOR_OVERLAP,
    COLOR_PATH,
    COLOR_START,
    COLOR_TEXT,
    COLOR_WARNING,
    COLOR_YELLOW,
    FPS,
    GRID_GAP,
    GRID_SIZE_OPTIONS,
    HABITAT_OPTIONS,
    MAX_PANEL_WIDTH,
    MIN_PANEL_WIDTH,
    OUTER_MARGIN,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATE_PLAYING,
    STATE_RESULT,
    STATE_START,
    TERRAIN_COLORS,
    TERRAIN_COSTS,
    WINDOW_TITLE,
)
from terrain import TerrainMap
from ui import Button, draw_label_value, draw_panel, draw_text, draw_wrapped_text


class TerrainPathGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_START

        self.selected_habitat = "Forest"
        self.selected_grid_size = 10
        self.terrain_map = None
        self.player = None
        self.optimal_path = []
        self.optimal_cost = 0
        self.player_cost = 0
        self.grade = "C Rank"
        self.won = False
        self.cost_difference = 0
        self.hover_cell = None

        self.habitat_buttons = {name: Button(name) for name in HABITAT_OPTIONS}
        self.size_buttons = {size: Button(f"{size}x{size}") for size in GRID_SIZE_OPTIONS}
        self.start_button = Button("Start Game")
        self.restart_button = Button("Play Again")
        self.clear_button = Button("Clear Path")
        self.submit_button = Button("Submit Path")

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_events()
            self.update(mouse_pos)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif self.state == STATE_START:
                self.handle_start_events(event)
            elif self.state == STATE_PLAYING:
                self.handle_play_events(event)
            elif self.state == STATE_RESULT:
                self.handle_result_events(event)

    def handle_start_events(self, event):
        for habitat, button in self.habitat_buttons.items():
            if button.handle_event(event):
                self.selected_habitat = habitat

        for size, button in self.size_buttons.items():
            if button.handle_event(event):
                self.selected_grid_size = size

        if self.start_button.handle_event(event):
            self.start_new_game()

    def handle_play_events(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        reached_end = self.player.has_reached_end(self.terrain_map.end)
        if self.submit_button.handle_event(event) and reached_end:
            self.finish_game()
            return

        if self.clear_button.handle_event(event):
            self.player.reset()
            return

        cell = self.cell_from_pos(event.pos)
        if cell is not None:
            self.player.handle_cell_click(cell, self.terrain_map)

    def handle_result_events(self, event):
        if self.restart_button.handle_event(event):
            self.start_new_game()

    def update(self, mouse_pos):
        if self.state == STATE_START:
            for button in self.habitat_buttons.values():
                button.update(mouse_pos)
            for button in self.size_buttons.values():
                button.update(mouse_pos)
            self.start_button.update(mouse_pos)
        elif self.state == STATE_PLAYING:
            self.clear_button.update(mouse_pos)
            self.submit_button.update(mouse_pos)
            self.hover_cell = self.cell_from_pos(mouse_pos)
        elif self.state == STATE_RESULT:
            self.restart_button.update(mouse_pos)
            self.hover_cell = None

    def start_new_game(self):
        self.terrain_map = TerrainMap(self.selected_grid_size, self.selected_habitat)
        self.player = PlayerPath(self.terrain_map.start)
        self.optimal_path, self.optimal_cost = compute_dijkstra(
            self.terrain_map.grid, self.terrain_map.start, self.terrain_map.end
        )
        self.player_cost = 0
        self.grade = "C Rank"
        self.won = False
        self.cost_difference = 0
        self.state = STATE_PLAYING

    def finish_game(self):
        self.player_cost = self.player.cost(self.terrain_map.grid)
        self.grade = get_grade(self.player_cost, self.optimal_cost)
        self.won = is_victory(self.player_cost, self.optimal_cost)
        self.cost_difference = self.player_cost - self.optimal_cost
        self.state = STATE_RESULT

    def draw(self):
        self.draw_background()
        if self.state == STATE_START:
            self.draw_start_screen()
        elif self.state == STATE_PLAYING:
            self.draw_game_screen(False)
        elif self.state == STATE_RESULT:
            self.draw_game_screen(True)
            self.draw_result_badge()

    def draw_background(self):
        self.screen.fill(COLOR_BG)
        w, h = self.screen.get_size()
        pygame.draw.rect(self.screen, COLOR_BG_2, (0, h // 2, w, h // 2))

    def draw_start_screen(self):
        w, h = self.screen.get_size()
        card = pygame.Rect(0, 0, min(560, w - 48), min(620, h - 48))
        card.center = (w // 2, h // 2)

        pygame.draw.rect(self.screen, (34, 42, 55), card, border_radius=24)
        pygame.draw.rect(self.screen, (71, 86, 110), card, width=2, border_radius=24)
        draw_text(self.screen, "Terrain Path", 48, COLOR_TEXT, center=(card.centerx, card.y + 70), bold=True)
        draw_text(self.screen, "Optimization Game", 36, COLOR_ACCENT, center=(card.centerx, card.y + 116), bold=True)
        draw_wrapped_text(
            self.screen,
            "Choose a habitat and grid size, then find the cheapest route before comparing your path with Dijkstra's optimal answer.",
            18,
            COLOR_MUTED,
            pygame.Rect(card.x + 54, card.y + 155, card.width - 108, 80),
        )

        y = card.y + 245
        draw_text(self.screen, "Habitat", 20, COLOR_TEXT, topleft=(card.x + 54, y), bold=True)
        self.layout_button_row(self.habitat_buttons.values(), card.x + 54, y + 36, card.width - 108)
        for name, button in self.habitat_buttons.items():
            button.selected = name == self.selected_habitat
            button.draw(self.screen)

        y += 125
        draw_text(self.screen, "Grid Size", 20, COLOR_TEXT, topleft=(card.x + 54, y), bold=True)
        self.layout_button_row(self.size_buttons.values(), card.x + 54, y + 36, card.width - 108)
        for size, button in self.size_buttons.items():
            button.selected = size == self.selected_grid_size
            button.draw(self.screen)

        self.start_button.set_rect((card.x + 54, card.bottom - 92, card.width - 108, BUTTON_HEIGHT + 8))
        self.start_button.selected = True
        self.start_button.draw(self.screen)

    def draw_game_screen(self, show_optimal):
        board_rect, panel_rect, cell_size = self.get_layout()
        self.draw_grid(board_rect, cell_size, show_optimal)
        self.draw_side_panel(panel_rect, show_optimal)

    def draw_grid(self, board_rect, cell_size, show_optimal):
        pygame.draw.rect(self.screen, (17, 21, 27), board_rect.inflate(10, 10), border_radius=18)

        for row in range(self.terrain_map.grid_size):
            for col in range(self.terrain_map.grid_size):
                cell = (row, col)
                rect = self.cell_rect(board_rect, cell_size, row, col)
                terrain = self.terrain_map.grid[row][col]
                radius = max(4, cell_size // 8)

                pygame.draw.rect(self.screen, TERRAIN_COLORS[terrain], rect, border_radius=radius)

                if self.hover_cell == cell and self.state == STATE_PLAYING:
                    self.draw_overlay(rect, COLOR_HOVER[:3], COLOR_HOVER[3])

                pygame.draw.rect(self.screen, COLOR_GRID_LINE, rect, width=1, border_radius=radius)

        overlap = self.get_overlap_edges(self.player.path, self.optimal_path) if show_optimal else set()
        if show_optimal:
            self.render_path(board_rect, cell_size, self.optimal_path, COLOR_OPTIMAL, 4, 12, COLOR_OPTIMAL_GLOW, overlap)
        self.render_path(board_rect, cell_size, self.player.path, COLOR_PATH, 9, 18, COLOR_PATH, overlap)
        self.draw_point(board_rect, cell_size, self.terrain_map.start, COLOR_START)
        self.draw_point(board_rect, cell_size, self.terrain_map.end, COLOR_END)

    def draw_overlay(self, rect, color, alpha):
        temp = pygame.Surface(rect.size, pygame.SRCALPHA)
        temp.fill((*color, alpha))
        self.screen.blit(temp, rect.topleft)

    def draw_path_line(self, start, end, color, width, glow=None):
        if glow is not None:
            pad = width + 12
            left = min(start[0], end[0]) - pad
            top = min(start[1], end[1]) - pad
            right = max(start[0], end[0]) + pad
            bottom = max(start[1], end[1]) + pad
            temp = pygame.Surface((right - left, bottom - top), pygame.SRCALPHA)
            a = (start[0] - left, start[1] - top)
            b = (end[0] - left, end[1] - top)
            pygame.draw.line(temp, (*glow, 60), a, b, width + 10)
            pygame.draw.circle(temp, (*glow, 60), a, (width + 10) // 2)
            pygame.draw.circle(temp, (*glow, 60), b, (width + 10) // 2)
            self.screen.blit(temp, (left, top))

        pygame.draw.line(self.screen, color, start, end, width)
        pygame.draw.circle(self.screen, color, start, width // 2)
        pygame.draw.circle(self.screen, color, end, width // 2)

    def draw_arrow(self, start, end, color, size):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        ux = dx / length
        uy = dy / length
        px = -uy
        py = ux
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        tip = (mid_x + ux * size * 0.62, mid_y + uy * size * 0.62)
        left = (mid_x - ux * size * 0.42 + px * size * 0.42, mid_y - uy * size * 0.42 + py * size * 0.42)
        right = (mid_x - ux * size * 0.42 - px * size * 0.42, mid_y - uy * size * 0.42 - py * size * 0.42)
        pygame.draw.polygon(self.screen, color, [tip, left, right])

    def render_path(self, board_rect, cell_size, path, color, width, arrow_size, glow=None, overlap=None):
        if len(path) < 2:
            return

        overlap = overlap or set()
        for i in range(len(path) - 1):
            curr = path[i]
            nxt = path[i + 1]
            start = self.cell_center(board_rect, cell_size, curr)
            end = self.cell_center(board_rect, cell_size, nxt)
            edge = self.edge_key(curr, nxt)
            seg_color = COLOR_OVERLAP if edge in overlap else color
            seg_width = width + 2 if edge in overlap else width
            seg_arrow = arrow_size + 3 if edge in overlap else arrow_size
            seg_glow = COLOR_OVERLAP if edge in overlap else glow

            self.draw_path_line(start, end, seg_color, seg_width, seg_glow)
            self.draw_arrow(start, end, seg_color, seg_arrow)

    def edge_key(self, first, second):
        return tuple(sorted((first, second)))

    def get_overlap_edges(self, first_path, second_path):
        first_edges = {
            self.edge_key(first_path[i], first_path[i + 1])
            for i in range(len(first_path) - 1)
        }
        second_edges = {
            self.edge_key(second_path[i], second_path[i + 1])
            for i in range(len(second_path) - 1)
        }
        return first_edges & second_edges

    def draw_point(self, board_rect, cell_size, cell, color):
        center = self.cell_center(board_rect, cell_size, cell)
        radius = max(7, cell_size // 4)
        pygame.draw.circle(self.screen, (15, 18, 24), center, radius + 4)
        pygame.draw.circle(self.screen, color, center, radius)

    def draw_side_panel(self, panel_rect, show_optimal):
        draw_panel(self.screen, panel_rect)
        x = panel_rect.x + 24
        y = panel_rect.y + 26
        content_w = panel_rect.width - 48
        title = "Results" if self.state == STATE_RESULT else "Route Builder"

        draw_text(self.screen, title, 30, COLOR_TEXT, topleft=(x, y), bold=True)
        y += 48
        info = f"{self.selected_habitat} habitat  |  {self.selected_grid_size}x{self.selected_grid_size}"
        draw_text(self.screen, info, 17, COLOR_MUTED, topleft=(x, y))
        y += 46

        if self.state == STATE_PLAYING:
            self.draw_play_panel(panel_rect, x, y, content_w)
        elif show_optimal:
            self.draw_result_panel(panel_rect, x, y, content_w)

    def draw_play_panel(self, panel_rect, x, y, content_w):
        can_submit = self.player.has_reached_end(self.terrain_map.end)
        draw_label_value(self.screen, "Current cost", str(self.player.cost(self.terrain_map.grid)), x, y, COLOR_YELLOW)

        y += 76
        draw_label_value(self.screen, "Selected tiles", str(len(self.player.path)), x, y, COLOR_ACCENT)

        y += 78
        self.draw_legend(x, y)

        y += 154
        self.draw_terrain_costs(x, y)

        draw_wrapped_text(
            self.screen,
            "Click adjacent non-water tiles. Submit becomes useful after reaching the red end tile.",
            16,
            COLOR_MUTED,
            pygame.Rect(x, panel_rect.bottom - 206, content_w, 58),
        )

        self.clear_button.set_rect((x, panel_rect.bottom - 138, content_w, BUTTON_HEIGHT))
        self.clear_button.selected = False
        self.clear_button.draw(self.screen)

        self.submit_button.set_rect((x, panel_rect.bottom - 80, content_w, BUTTON_HEIGHT))
        self.submit_button.selected = can_submit
        self.submit_button.draw(self.screen)

        if not can_submit:
            draw_text(
                self.screen,
                "Reach the end first",
                15,
                COLOR_MUTED,
                center=(self.submit_button.rect.centerx, self.submit_button.rect.bottom + 16),
            )

    def draw_result_panel(self, panel_rect, x, y, content_w):
        draw_label_value(self.screen, "Player cost", str(self.player_cost), x, y, COLOR_YELLOW)
        draw_label_value(self.screen, "Optimal cost", str(self.optimal_cost), x + content_w // 2, y, COLOR_OPTIMAL_GLOW)

        y += 82
        diff_text = f"+{self.cost_difference}" if self.cost_difference > 0 else "0"
        diff_color = COLOR_WARNING if self.cost_difference else COLOR_ACCENT
        draw_label_value(self.screen, "Difference", diff_text, x, y, diff_color)
        draw_label_value(self.screen, "Grade", self.grade, x + content_w // 2, y, grade_color(self.grade))

        y += 88
        msg = "Victory!" if self.won else "Failure"
        msg_color = COLOR_ACCENT if self.won else COLOR_WARNING
        draw_text(self.screen, msg, 28, msg_color, topleft=(x, y), bold=True)
        draw_wrapped_text(self.screen, self.learning_feedback(), 17, COLOR_MUTED, pygame.Rect(x, y + 40, content_w, 96))

        y += 152
        self.draw_legend(x, y)

        self.restart_button.set_rect((x, panel_rect.bottom - 80, content_w, BUTTON_HEIGHT))
        self.restart_button.selected = True
        self.restart_button.draw(self.screen)

    def draw_terrain_costs(self, x, y):
        draw_text(self.screen, "Terrain Costs", 20, COLOR_TEXT, topleft=(x, y), bold=True)
        y += 34
        for terrain, cost in TERRAIN_COSTS.items():
            pygame.draw.rect(self.screen, TERRAIN_COLORS[terrain], (x, y + 4, 18, 18), border_radius=5)
            cost_text = "Blocked" if cost is None else str(cost)
            draw_text(self.screen, f"{terrain.title()}: {cost_text}", 17, COLOR_MUTED, topleft=(x + 30, y))
            y += 26

    def draw_legend(self, x, y):
        items = [
            ("Player Path", COLOR_PATH, "line"),
            ("Optimal Path", COLOR_OPTIMAL_GLOW, "line"),
            ("Start", COLOR_START, "circle"),
            ("End", COLOR_END, "circle"),
        ]

        draw_text(self.screen, "Legend", 20, COLOR_TEXT, topleft=(x, y), bold=True)
        y += 34

        for label, color, shape in items:
            if shape == "circle":
                pygame.draw.circle(self.screen, color, (x + 10, y + 13), 9)
            else:
                start = (x, y + 13)
                end = (x + 22, y + 13)
                self.draw_path_line(start, end, color, 4)
                self.draw_arrow(start, end, color, 8)
            draw_text(self.screen, label, 17, COLOR_MUTED, topleft=(x + 32, y))
            y += 28

    def learning_feedback(self):
        if self.cost_difference == 0:
            return "Perfect route! You found the optimal path."
        if self.cost_difference <= 5:
            return "Very efficient path. Compare with the optimal route."
        return "There was a shorter route available. Study the highlighted optimal path."

    def draw_result_badge(self):
        board_rect, _, _ = self.get_layout()
        panel = pygame.Rect(0, 0, min(360, board_rect.width - 32), 92)
        panel.midtop = (board_rect.centerx, max(14, board_rect.y + 16))

        pygame.draw.rect(self.screen, (29, 36, 48), panel, border_radius=22)
        pygame.draw.rect(self.screen, (83, 99, 126), panel, width=2, border_radius=22)

        msg = "Victory!" if self.won else "Try Again"
        msg_color = COLOR_ACCENT if self.won else COLOR_WARNING
        draw_text(self.screen, msg, 28, msg_color, center=(panel.centerx, panel.y + 28), bold=True)
        draw_text(
            self.screen,
            f"{self.grade}  |  Difference: +{self.cost_difference}",
            18,
            grade_color(self.grade),
            center=(panel.centerx, panel.y + 62),
            bold=True,
        )

    def layout_button_row(self, buttons, x, y, width):
        buttons = list(buttons)
        gap = 12
        button_w = (width - gap * (len(buttons) - 1)) // len(buttons)
        for i, button in enumerate(buttons):
            button.set_rect((x + i * (button_w + gap), y, button_w, BUTTON_HEIGHT))

    def get_layout(self):
        w, h = self.screen.get_size()
        panel_w = min(MAX_PANEL_WIDTH, max(MIN_PANEL_WIDTH, int(w * 0.3)))
        board_w = w - panel_w - OUTER_MARGIN * 3
        board_h = h - OUTER_MARGIN * 2
        cell_size = max(24, min(board_w, board_h) // self.terrain_map.grid_size)
        board_size = cell_size * self.terrain_map.grid_size

        board_rect = pygame.Rect(OUTER_MARGIN, (h - board_size) // 2, board_size, board_size)
        panel_rect = pygame.Rect(
            board_rect.right + OUTER_MARGIN,
            OUTER_MARGIN,
            w - board_rect.right - OUTER_MARGIN * 2,
            h - OUTER_MARGIN * 2,
        )
        return board_rect, panel_rect, cell_size

    def cell_rect(self, board_rect, cell_size, row, col):
        return pygame.Rect(
            board_rect.x + col * cell_size + GRID_GAP,
            board_rect.y + row * cell_size + GRID_GAP,
            cell_size - GRID_GAP * 2,
            cell_size - GRID_GAP * 2,
        )

    def cell_center(self, board_rect, cell_size, cell):
        row, col = cell
        return (
            board_rect.x + col * cell_size + cell_size // 2,
            board_rect.y + row * cell_size + cell_size // 2,
        )

    def cell_from_pos(self, pos):
        if self.terrain_map is None:
            return None

        board_rect, _, cell_size = self.get_layout()
        if not board_rect.collidepoint(pos):
            return None

        col = (pos[0] - board_rect.x) // cell_size
        row = (pos[1] - board_rect.y) // cell_size
        cell = (int(row), int(col))

        if 0 <= cell[0] < self.terrain_map.grid_size and 0 <= cell[1] < self.terrain_map.grid_size:
            return cell
        return None


def main():
    game = TerrainPathGame()
    game.run()


if __name__ == "__main__":
    main()
