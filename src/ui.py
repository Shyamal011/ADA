import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TERRAIN_COLORS = {
    "grass": (50, 200, 50),
    "forest": (16, 120, 16),
    "mountain": (120, 120, 120),
    "water": (40, 80, 255),
    "sand": (220, 200, 120)
}

PATH_COLOR = (255, 255, 0)

CELL_SIZE = 50


def draw_grid(screen, grid, player_path):

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):

            terrain = grid[r][c]

            color = TERRAIN_COLORS[terrain]

            rect = pygame.Rect(
                c * CELL_SIZE,
                r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(screen, BLACK, rect, 1)

            if (r, c) in player_path:

                pygame.draw.rect(
                    screen,
                    PATH_COLOR,
                    rect,
                    4
                )


def draw_text(screen, text, x, y, font):

    surface = font.render(text, True, BLACK)

    screen.blit(surface, (x, y))