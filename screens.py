# screens.py
"""
Handles drawing the different game screens: Home, Colour Settings, Game.
Positions elements relative to current window size. Adds 'Back' button to game screen.
Uses British English spelling (colour).
"""
import pygame
import settings
import ui # Import the ui module for buttons and text drawing
from settings import GameState # Import GameState enum

def draw_home_screen(surface, play_action, colour_action):
    """
    Draws the home screen with Play and Colour Schemes buttons.
    Positions elements relative to current window size.

    Args:
        surface: The pygame surface to draw on.
        play_action: Function to call when Play button is clicked.
        colour_action: Function to call when Colour Schemes button is clicked.
    """
    surface.fill(settings.THEME["background"])
    width = surface.get_width()
    height = surface.get_height()

    # Title
    title_rect = ui.draw_text(surface, "Minesweeper", settings.FONT_LARGE, settings.THEME["text"],
                              width // 2, height // 4, center=True)

    # Buttons
    button_width = 250
    button_height = 60
    button_spacing = 30
    button_y_start = title_rect.bottom + 50

    # Play Button
    ui.button(surface, "Play Game",
              width // 2 - button_width // 2, button_y_start,
              button_width, button_height,
              action=play_action, font=settings.FONT_MEDIUM)

    # Colour Schemes Button
    ui.button(surface, "Colour Schemes",
              width // 2 - button_width // 2, button_y_start + button_height + button_spacing,
              button_width, button_height,
              action=colour_action, font=settings.FONT_MEDIUM)


def draw_colour_settings_screen(surface, back_action):
    """
    Draws the colour settings screen with theme selection buttons.
    Positions elements relative to current window size.

    Args:
        surface: The pygame surface to draw on.
        back_action: Function to call when the Back button is clicked.
    """
    surface.fill(settings.THEME["background"])
    width = surface.get_width()
    height = surface.get_height()

    # Title
    title_rect = ui.draw_text(surface, "Select Colour Scheme", settings.FONT_LARGE, settings.THEME["text"],
                              width // 2, height // 8, center=True)

    # Theme Buttons Layout
    button_width = 200
    button_height = 50
    button_padding_x = 40
    button_padding_y = 25
    max_buttons_per_row = 3 # Adjust based on desired layout / window width potentially
    num_buttons = len(settings.COLOUR_THEMES)
    num_rows = (num_buttons + max_buttons_per_row - 1) // max_buttons_per_row

    # Calculate dynamic starting position to center the button grid
    total_grid_width = max_buttons_per_row * button_width + (max_buttons_per_row - 1) * button_padding_x
    start_x = max(20, (width - total_grid_width) // 2) # Ensure some padding from edge
    start_y = title_rect.bottom + 50

    current_col = 0
    current_row = 0
    for i, theme_name in enumerate(settings.COLOUR_THEMES.keys()):
        button_x = start_x + current_col * (button_width + button_padding_x)
        button_y = start_y + current_row * (button_height + button_padding_y)

        # Highlight the currently selected theme
        is_selected = (theme_name == settings.CURRENT_THEME_NAME)
        # Use smaller font if selected text is too long? For now, keep it simple.
        button_text = f"{theme_name}{' (Selected)' if is_selected else ''}"

        # Define the action for this button: set the theme
        theme_action = lambda name=theme_name: settings.set_theme(name)

        ui.button(surface, button_text, button_x, button_y, button_width, button_height,
                  action=theme_action, font=settings.FONT_SMALL, center_text=True) # Center text

        current_col += 1
        if current_col >= max_buttons_per_row:
            current_col = 0
            current_row += 1

    # Back Button (position near bottom center)
    ui.button(surface, "Back",
              width // 2 - 100, height - 80, # Position near bottom center
              200, 50,
              action=back_action, font=settings.FONT_MEDIUM)


def draw_game_screen(surface, board, reset_action, back_action):
    """
    Draws the main game screen, including the board, status messages,
    and Reset/Back buttons.

    Args:
        surface: The pygame surface to draw on.
        board: The Minesweeper Board object.
        reset_action: Function to call when the Reset button is clicked (if game over/won).
        back_action: Function to call when the Back to Home button is clicked.
    """
    surface.fill(settings.THEME["background"])
    width = surface.get_width()
    # height = surface.get_height() # Not currently used here

    # --- Draw Board ---
    # The board's draw method uses settings.GAME_AREA_X/Y which are updated on resize
    board.draw(surface)

    # --- Draw Status Messages & Reset Button (if applicable) ---
    message = None
    message_rect = None
    if board.game_won:
        message = "Congratulations! You Won!"
    elif board.game_over: # Check this after won, as won also sets game_over
        message = "Game Over! You hit a mine."

    if message:
        # Display message centrally above the board (using board's Y position)
        message_rect = ui.draw_text(surface, message, settings.FONT_MEDIUM, settings.THEME["text"],
                                    width // 2, settings.GAME_AREA_Y // 2 + 10, center=True) # Adjusted Y slightly

        # Add a Reset button below the message
        ui.button(surface, "Play Again",
                  width // 2 - 100, message_rect.bottom + 20,
                  200, 50,
                  action=reset_action, font=settings.FONT_MEDIUM)

    # --- Draw Back Button (Always visible on game screen) ---
    # Position top-left, with some padding
    back_button_width = 120
    back_button_height = 40
    ui.button(surface, "Back to Home",
              20, 20, # Top-left corner padding
              back_button_width, back_button_height,
              action=back_action, font=settings.FONT_SMALL)



