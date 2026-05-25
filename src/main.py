import pygame

from ui import *
from player import *

pygame.init()

WIDTH = 800
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(
    "Terrain Path Game"
)

font = pygame.font.SysFont(None, 36)

grid = [
    ["grass", "grass", "forest", "grass"],
    ["water", "mountain", "grass", "grass"],
    ["grass", "grass", "forest", "grass"],
    ["grass", "water", "grass", "grass"]
]

player_path = []

running = True

while running:

    screen.fill(WHITE)

    draw_grid(screen, grid, player_path)

    draw_text(
        screen,
        "Click tiles to build path",
        20,
        620,
        font
    )

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            if row < len(grid) and col < len(grid[0]):

                clicked_cell = (row, col)

                player_path = add_to_path(
                    player_path,
                    clicked_cell,
                    grid
                )

    pygame.display.update()

pygame.quit()