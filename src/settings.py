SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 760
FPS = 60
WINDOW_TITLE = "Terrain Path Optimization Game"

STATE_START = "start"
STATE_PLAYING = "playing"
STATE_RESULT = "result"

MIN_PANEL_WIDTH = 280
MAX_PANEL_WIDTH = 340
OUTER_MARGIN = 28
GRID_GAP = 2
BUTTON_HEIGHT = 48

TERRAIN_COSTS = {
    "grass": 1,
    "forest": 3,
    "sand": 4,
    "snow": 5,
    "mountain": 7,
    "water": None,
}

TERRAIN_COLORS = {
    "grass": (102, 180, 95),
    "forest": (42, 122, 78),
    "mountain": (122, 118, 112),
    "water": (55, 130, 188),
    "sand": (212, 181, 104),
    "snow": (218, 232, 238),
}

HABITAT_OPTIONS = ["Forest", "Desert", "Snow"]
GRID_SIZE_OPTIONS = [5, 10, 15]

HABITAT_TERRAIN_WEIGHTS = {
    "Forest": {
        "grass": 34,
        "forest": 36,
        "mountain": 12,
        "water": 10,
        "sand": 4,
        "snow": 4,
    },
    "Desert": {
        "sand": 44,
        "grass": 18,
        "mountain": 16,
        "water": 6,
        "forest": 8,
        "snow": 8,
    },
    "Snow": {
        "snow": 42,
        "forest": 18,
        "mountain": 16,
        "water": 9,
        "grass": 12,
        "sand": 3,
    },
}

HABITAT_START_TERRAIN = {
    "Forest": "grass",
    "Desert": "sand",
    "Snow": "snow",
}

COLOR_BG = (21, 25, 32)
COLOR_BG_2 = (29, 35, 45)
COLOR_PANEL_LIGHT = (47, 56, 72)
COLOR_TEXT = (238, 242, 247)
COLOR_MUTED = (163, 174, 190)
COLOR_ACCENT = (94, 210, 166)
COLOR_ACCENT_DARK = (57, 157, 123)
COLOR_WARNING = (239, 113, 113)
COLOR_YELLOW = (241, 196, 91)
COLOR_GRID_LINE = (29, 34, 43)
COLOR_PATH = (255, 232, 115)
COLOR_OPTIMAL = (137, 110, 255)
COLOR_OPTIMAL_GLOW = (87, 221, 255)
COLOR_OVERLAP = (180, 247, 231)
COLOR_HOVER = (255, 255, 255, 44)
COLOR_SELECTED_OUTLINE = (255, 244, 175)
COLOR_START = (66, 220, 132)
COLOR_END = (248, 91, 99)

RANK_COLORS = {
    "S Rank": (94, 210, 166),
    "A Rank": (110, 190, 255),
    "B Rank": (241, 196, 91),
    "C Rank": (239, 113, 113),
}
