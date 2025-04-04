# Pygame Minesweeper

A classic implementation of the Minesweeper game built using Python and the Pygame library.

## Features

* Classic Minesweeper gameplay.
* Adjustable grid size and mine count (via `settings.py`).
* Home screen with options to Play or change settings.
* Multiple fruit-themed colour schemes to choose from.
* Clean, multi-file structure.

## Requirements

* Python 3.x
* Pygame library

## Installation

1.  **Ensure Python 3 is installed.** You can download it from [python.org](https://www.python.org/).
2.  **Install Pygame:** Open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```
    *(On some systems, you might need to use `pip3` instead of `pip`)*

## How to Run

1.  Save all the provided Python files (`main.py`, `settings.py`, `ui.py`, `board.py`, `screens.py`) in the same directory.
2.  Navigate to that directory in your terminal or command prompt.
3.  Run the main script:
    ```bash
    python main.py
    ```
    *(Or `python3 main.py` depending on your system)*

## Gameplay

* **Objective:** Reveal all the cells on the grid that do *not* contain mines.
* **Controls:**
    * **Left Click:** Reveal a cell.
        * If you click a mine, the game is over.
        * If you click a cell with a number, it indicates how many mines are adjacent (horizontally, vertically, or diagonally) to that cell.
        * If you click an empty cell (no adjacent mines), it will automatically reveal all adjacent empty cells and numbered cells bordering them.
    * **Right Click:** Place or remove a flag on a hidden cell. Flags are used to mark suspected mine locations. You cannot reveal a flagged cell with a left click.
* **Winning:** You win the game when all non-mine cells have been revealed.
* **Losing:** You lose the game if you reveal a cell containing a mine.

## Customisation

* **Grid Size & Mines:** You can change the `GRID_ROWS`, `GRID_COLS`, and `NUM_MINES` constants in the `settings.py` file to alter the difficulty.
* **Colour Schemes:** Select different visual themes from the "Colour Schemes" menu accessible from the home screen. New themes can potentially be added by defining them in the `COLOUR_THEMES` dictionary within `settings.py`.

## File Structure

* `main.py`: Main game loop, event handling, state management.
* `settings.py`: Game constants, dimensions, colours, themes, fonts.
* `board.py`: Contains the `Board` class handling all game logic (mine placement, revealing, flagging, win/loss).
* `ui.py`: Helper functions for drawing UI elements like text and buttons.
* `screens.py`: Functions to draw the different game screens (Home, Colour Settings, Game).
