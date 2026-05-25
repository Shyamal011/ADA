import pygame

from settings import (
    BUTTON_HEIGHT,
    COLOR_ACCENT,
    COLOR_ACCENT_DARK,
    COLOR_MUTED,
    COLOR_PANEL_LIGHT,
    COLOR_TEXT,
)


def get_font(size, bold=False):
    return pygame.font.SysFont("segoeui", size, bold=bold) or pygame.font.SysFont(
        "arial", size, bold=bold
    )


def draw_text(surface, text, size, color, center=None, topleft=None, bold=False):
    font = get_font(size, bold)
    img = font.render(str(text), True, color)
    rect = img.get_rect()

    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft

    surface.blit(img, rect)
    return rect


def draw_wrapped_text(surface, text, size, color, rect, line_gap=6, bold=False):
    font = get_font(size, bold)
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = word if line == "" else line + " " + word
        if font.size(test)[0] <= rect.width:
            line = test
        else:
            lines.append(line)
            line = word

    if line:
        lines.append(line)

    y = rect.y
    for line in lines:
        img = font.render(line, True, color)
        surface.blit(img, (rect.x, y))
        y += img.get_height() + line_gap


class Button:
    def __init__(self, text, rect=None, selected=False):
        self.text = text
        self.rect = pygame.Rect(rect or (0, 0, 160, BUTTON_HEIGHT))
        self.selected = selected
        self.hover_amount = 0.0

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect)

    def update(self, mouse_pos):
        target = 1.0 if self.rect.collidepoint(mouse_pos) else 0.0
        self.hover_amount += (target - self.hover_amount) * 0.2

    def handle_event(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

    def draw(self, surface):
        if self.selected:
            base = COLOR_ACCENT_DARK
            border = COLOR_ACCENT
        else:
            base = COLOR_PANEL_LIGHT
            border = (88, 100, 122)

        lift = int(18 * self.hover_amount)
        color = tuple(min(255, c + lift) for c in base)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, border, self.rect, width=2, border_radius=12)
        draw_text(surface, self.text, 20, COLOR_TEXT, center=self.rect.center, bold=True)


def draw_panel(surface, rect):
    pygame.draw.rect(surface, (31, 38, 49), rect, border_radius=18)
    pygame.draw.rect(surface, (38, 46, 60), rect.inflate(-4, -4), border_radius=16)


def draw_label_value(surface, label, value, x, y, color=COLOR_TEXT):
    draw_text(surface, label, 17, COLOR_MUTED, topleft=(x, y))
    draw_text(surface, value, 22, color, topleft=(x, y + 22), bold=True)
