# settings.py
"""
Stores game constants, settings, and colour themes for Minesweeper.
Includes function to update game area position based on window size.
Uses British English spelling (colour).
"""
import pygame

# --- Screen Dimensions (Initial) ---
# These can be updated if the window is resized
WIDTH = 800
HEIGHT = 650
FPS = 60

# --- Grid Settings (Fixed Size) ---
GRID_ROWS = 16
GRID_COLS = 16
NUM_MINES = 40
# Calculate cell size based on a designated game area size
# Keep the game area itself fixed for simplicity with resizing window
_FIXED_GAME_AREA_WIDTH = 600
_FIXED_GAME_AREA_HEIGHT = 600
CELL_WIDTH = _FIXED_GAME_AREA_WIDTH // GRID_COLS
CELL_HEIGHT = _FIXED_GAME_AREA_HEIGHT // GRID_ROWS
# Ensure cells are square if possible, using the smaller dimension
CELL_SIZE = min(CELL_WIDTH, CELL_HEIGHT)
# Recalculate actual game area based on cell size
GAME_AREA_WIDTH = CELL_SIZE * GRID_COLS
GAME_AREA_HEIGHT = CELL_SIZE * GRID_ROWS

# --- Game Area Position (Calculated dynamically) ---
# Initial calculation, will be updated on resize
GAME_AREA_X = (WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = (HEIGHT - GAME_AREA_HEIGHT) // 2 + 25 # Offset for potential top bar

def update_game_area_position():
    """Recalculates the top-left corner (X, Y) of the game area to keep it centred."""
    global GAME_AREA_X, GAME_AREA_Y
    GAME_AREA_X = (WIDTH - GAME_AREA_WIDTH) // 2
    GAME_AREA_Y = (HEIGHT - GAME_AREA_HEIGHT) // 2 + 25 # Keep the vertical offset


# --- Colours (RGB Tuples) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# --- Colour Themes ---
# Structure: name: {element: colour}
COLOUR_THEMES = {
    "Classic": {
        "background": (220, 220, 220),
        "grid_lines": DARK_GRAY,
        "cell_hidden": GRAY,
        "cell_revealed": (211, 211, 211),
        "cell_hover": (170, 170, 170),
        "text": BLACK,
        "button_bg": GRAY,
        "button_hover": DARK_GRAY,
        "button_text": BLACK,
        "flag": RED,
        "mine": BLACK,
        "numbers": { # Colours for numbers 1-8
            1: (0, 0, 255),    # Blue
            2: (0, 128, 0),    # Green
            3: (255, 0, 0),    # Red
            4: (0, 0, 128),    # Dark Blue
            5: (128, 0, 0),    # Dark Red
            6: (0, 128, 128),  # Teal
            7: (0, 0, 0),      # Black
            8: (128, 128, 128) # Gray
        }
    },
    "Strawberry": {
        "background": (255, 223, 223), # Light pink
        "grid_lines": (139, 0, 0),     # Dark Red
        "cell_hidden": (255, 99, 71),  # Tomato Red
        "cell_revealed": (255, 192, 203),# Pink
        "cell_hover": (255, 60, 40),
        "text": (139, 0, 0),
        "button_bg": (255, 99, 71),
        "button_hover": (233, 150, 122), # Dark Salmon
        "button_text": WHITE,
        "flag": (0, 100, 0),      # Dark Green (for contrast)
        "mine": (50, 50, 50),
        "numbers": {
            1: (0, 0, 139), 2: (0, 100, 0), 3: (139, 0, 0), 4: (75, 0, 130),
            5: (165, 42, 42), 6: (46, 139, 87), 7: (40, 40, 40), 8: (100, 100, 100)
        }
    },
    "Lemon": {
        "background": (255, 255, 224), # Light Yellow
        "grid_lines": (184, 134, 11),  # Dark Goldenrod
        "cell_hidden": (255, 255, 0),  # Yellow
        "cell_revealed": (255, 250, 205),# Lemon Chiffon
        "cell_hover": (240, 230, 140), # Khaki
        "text": (139, 69, 19),    # Saddle Brown
        "button_bg": (255, 215, 0),  # Gold
        "button_hover": (218, 165, 32), # Goldenrod
        "button_text": BLACK,
        "flag": (0, 128, 0),      # Green
        "mine": (30, 30, 30),
        "numbers": {
            1: (0, 0, 205), 2: (50, 205, 50), 3: (205, 92, 92), 4: (72, 61, 139),
            5: (139, 69, 19), 6: (47, 79, 79), 7: (60, 60, 60), 8: (112, 128, 144)
        }
    },
    "Lime": {
        "background": (240, 255, 240), # Honeydew
        "grid_lines": (0, 100, 0),     # Dark Green
        "cell_hidden": (50, 205, 50),  # Lime Green
        "cell_revealed": (152, 251, 152),# Pale Green
        "cell_hover": (34, 139, 34),   # Forest Green
        "text": (0, 100, 0),
        "button_bg": (124, 252, 0),  # Lawn Green
        "button_hover": (173, 255, 47), # Green Yellow
        "button_text": BLACK,
        "flag": (255, 165, 0),    # Orange (for contrast)
        "mine": (40, 40, 40),
        "numbers": {
            1: (30, 144, 255), 2: (128, 0, 128), 3: (255, 0, 0), 4: (0, 0, 139),
            5: (160, 82, 45), 6: (0, 139, 139), 7: (50, 50, 50), 8: (105, 105, 105)
        }
    },
    "Blueberry": {
        "background": (240, 248, 255), # Alice Blue
        "grid_lines": (0, 0, 139),     # Dark Blue
        "cell_hidden": (100, 149, 237),# Cornflower Blue
        "cell_revealed": (173, 216, 230),# Light Blue
        "cell_hover": (70, 130, 180),  # Steel Blue
        "text": (25, 25, 112),    # Midnight Blue
        "button_bg": (65, 105, 225),   # Royal Blue
        "button_hover": (100, 149, 237), # Cornflower Blue
        "button_text": WHITE,
        "flag": (255, 215, 0),    # Gold
        "mine": (10, 10, 10),
        "numbers": {
            1: (255, 140, 0), 2: (34, 139, 34), 3: (220, 20, 60), 4: (148, 0, 211),
            5: (210, 105, 30), 6: (0, 206, 209), 7: (70, 70, 70), 8: (169, 169, 169)
        }
    },
    "Orange": {
        "background": (255, 245, 238), # Seashell
        "grid_lines": (160, 82, 45),   # Sienna
        "cell_hidden": (255, 165, 0),  # Orange
        "cell_revealed": (255, 228, 181),# Moccasin
        "cell_hover": (255, 140, 0),   # Dark Orange
        "text": (139, 69, 19),    # Saddle Brown
        "button_bg": (255, 127, 80),   # Coral
        "button_hover": (255, 99, 71),   # Tomato
        "button_text": WHITE,
        "flag": (0, 0, 205),      # Medium Blue
        "mine": (50, 20, 0),
        "numbers": {
            1: (0, 191, 255), 2: (154, 205, 50), 3: (255, 69, 0), 4: (75, 0, 130),
            5: (128, 0, 0), 6: (0, 128, 128), 7: (60, 60, 60), 8: (119, 136, 153)
        }
    },
    "Grape": {
        "background": (230, 230, 250), # Lavender
        "grid_lines": (75, 0, 130),    # Indigo
        "cell_hidden": (147, 112, 219),# Medium Purple
        "cell_revealed": (216, 191, 216),# Thistle
        "cell_hover": (138, 43, 226),  # Blue Violet
        "text": (48, 25, 52),     # Dark Purple
        "button_bg": (153, 50, 204),   # Dark Orchid
        "button_hover": (148, 0, 211),   # Dark Violet
        "button_text": WHITE,
        "flag": (255, 255, 0),    # Yellow
        "mine": (20, 0, 30),
        "numbers": {
            1: (0, 255, 127), 2: (255, 105, 180), 3: (255, 69, 0), 4: (0, 100, 0),
            5: (178, 34, 34), 6: (72, 209, 204), 7: (80, 80, 80), 8: (188, 143, 143)
        }
    },
     "Watermelon": {
        "background": (240, 255, 240), # Honeydew
        "grid_lines": (0, 100, 0),     # Dark Green
        "cell_hidden": (255, 105, 180),# Hot Pink
        "cell_revealed": (255, 182, 193),# Light Pink
        "cell_hover": (255, 20, 147),  # Deep Pink
        "text": (0, 100, 0),      # Dark Green
        "button_bg": (60, 179, 113),   # Medium Sea Green
        "button_hover": (46, 139, 87),   # Sea Green
        "button_text": WHITE,
        "flag": (50, 50, 50),      # Dark Gray (seeds)
        "mine": (0, 0, 0),         # Black (seeds)
        "numbers": {
            1: (0, 0, 255), 2: (0, 128, 0), 3: (255, 0, 0), 4: (0, 0, 139),
            5: (139, 0, 0), 6: (0, 139, 139), 7: (40, 40, 40), 8: (100, 100, 100)
        }
    }
}

# --- Current Theme ---
# Start with the Classic theme
CURRENT_THEME_NAME = "Classic"
THEME = COLOUR_THEMES[CURRENT_THEME_NAME]

def set_theme(theme_name):
    """Updates the global THEME variable."""
    global CURRENT_THEME_NAME, THEME
    if theme_name in COLOUR_THEMES:
        CURRENT_THEME_NAME = theme_name
        THEME = COLOUR_THEMES[theme_name]
        print(f"Theme set to: {theme_name}") # For debugging
    else:
        print(f"Warning: Theme '{theme_name}' not found. Using default.")
        CURRENT_THEME_NAME = "Classic"
        THEME = COLOUR_THEMES["Classic"]


# --- Fonts (Fixed size for simplicity with resizing) ---
pygame.font.init() # Initialise font module
try:
    # Try using a common sans-serif font
    FONT_NAME = pygame.font.match_font('arial', bold=True)
    if FONT_NAME is None:
        FONT_NAME = pygame.font.get_default_font()

    # Define font sizes (kept fixed for now)
    FONT_LARGE = pygame.font.Font(FONT_NAME, 48)
    FONT_MEDIUM = pygame.font.Font(FONT_NAME, 30)
    FONT_SMALL = pygame.font.Font(FONT_NAME, 20)
    FONT_CELL = pygame.font.Font(FONT_NAME, int(CELL_SIZE * 0.6)) # Font size relative to cell size
except Exception as e:
    print(f"Error loading font: {e}")
    # Fallback to default font if specific one fails
    FONT_NAME = pygame.font.get_default_font()
    FONT_LARGE = pygame.font.Font(FONT_NAME, 48)
    FONT_MEDIUM = pygame.font.Font(FONT_NAME, 30)
    FONT_SMALL = pygame.font.Font(FONT_NAME, 20)
    FONT_CELL = pygame.font.Font(FONT_NAME, int(CELL_SIZE * 0.6))


# --- Game States ---
class GameState:
    HOME = 0
    COLOUR_SETTINGS = 1
    PLAYING = 2
    # GAME_OVER and WON are now handled implicitly by board state within PLAYING state

# --- Cell States ---
class CellState:
    HIDDEN = 0
    REVEALED = 1
    FLAGGED = 2

# --- Other Constants ---
MINE_VALUE = -1 # Value in the grid indicating a mine
