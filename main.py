# main.py
"""
Main entry point for the Pygame Minesweeper game.
Handles game initialisation, the main loop, event handling (including window resize),
and switching between different game screens/states. Adds 'Back' button functionality.
Uses British English spelling (colour).
"""
import pygame
import sys
import settings # Import settings for constants and theme management
import screens # Import screen drawing functions
from board import Board # Import the Board class
from settings import GameState # Import the GameState enum

def main():
    """Initialises Pygame, sets up the game, and runs the main loop."""
    pygame.init()
    pygame.font.init() # Ensure font module is initialised

    # --- Screen Setup ---
    # Use current settings dimensions and add RESIZABLE flag
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    # --- Game Variables ---
    current_state = GameState.HOME
    game_board = None # Initialise board only when 'Play' is clicked

    # --- Action Functions (defined once) ---
    def go_to_home():
        nonlocal current_state, game_board
        print("Going back home...")
        current_state = GameState.HOME
        game_board = None # Discard current board when going home

    def go_to_play():
        nonlocal current_state, game_board
        print("Starting new game...")
        # Ensure game area position is correct before creating board
        settings.update_game_area_position()
        game_board = Board(settings.GRID_ROWS, settings.GRID_COLS, settings.NUM_MINES)
        current_state = GameState.PLAYING

    def go_to_colours():
        nonlocal current_state
        print("Going to colour settings...")
        current_state = GameState.COLOUR_SETTINGS

    def reset_game():
        nonlocal game_board
        if game_board: # Only reset if board exists
            print("Resetting game...")
            game_board.reset()
            # State remains PLAYING

    # --- Main Game Loop ---
    running = True
    while running:
        # --- Event Handling ---
        # Get mouse state once per frame for potentially better button handling
        mouse_pos = pygame.mouse.get_pos()
        # mouse_buttons = pygame.mouse.get_pressed() # (left, middle, right)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                # Update settings dimensions
                settings.WIDTH = event.w
                settings.HEIGHT = event.h
                # Recreate the screen surface with the new size
                screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.RESIZABLE)
                # Recalculate game area centering
                settings.update_game_area_position()
                print(f"Window resized to: {settings.WIDTH}x{settings.HEIGHT}") # Debugging

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle board clicks only in PLAYING state
                if current_state == GameState.PLAYING and game_board:
                    # Pass current mouse pos from event
                    game_board.handle_click(event.pos, event.button)


        # --- State Management & Drawing ---
        # Reload theme settings in case they changed via Colour Settings screen
        active_theme = settings.THEME

        # --- Screen Drawing ---
        screen.fill(active_theme["background"]) # Clear screen with current theme bg

        if current_state == GameState.HOME:
            screens.draw_home_screen(screen, go_to_play, go_to_colours)

        elif current_state == GameState.COLOUR_SETTINGS:
            screens.draw_colour_settings_screen(screen, go_to_home) # Pass go_to_home as back action

        elif current_state == GameState.PLAYING:
            if game_board:
                 # Pass reset_game and go_to_home actions
                screens.draw_game_screen(screen, game_board, reset_game, go_to_home)

            else:
                # Fallback if board somehow doesn't exist in PLAYING state
                print("Error: In PLAYING state but no game_board exists. Returning home.")
                go_to_home()


        # --- Update Display ---
        pygame.display.flip()

        # --- Frame Rate Control ---
        clock.tick(settings.FPS)

    # --- Quit Pygame ---
    pygame.quit()
    sys.exit()

# --- Run the Game ---
if __name__ == '__main__':
    main()
