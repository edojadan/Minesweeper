# board.py
"""
Contains the Board class for Minesweeper game logic.
Handles mine placement, cell revealing, flagging, and win/loss conditions.
Uses British English spelling (colour).
Uses updated settings for board positioning.
"""
import pygame
import random
import settings # Import settings for grid dimensions, colours, etc.
from settings import CellState # Import CellState enum
import ui # Import ui for drawing text

class Board:
    """Represents the Minesweeper game board and its logic."""

    def __init__(self, rows, cols, mines):
        """
        Initialise the board.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
            mines (int): Number of mines to place on the board.
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.cell_states = [[CellState.HIDDEN for _ in range(cols)] for _ in range(rows)]
        self.flags_placed = 0
        self.mines_location = set()
        self.first_click = True
        self.game_over = False
        self.game_won = False

        # Get fixed cell size and board pixel dimensions from settings
        self.cell_size = settings.CELL_SIZE
        self.board_pixel_width = settings.GAME_AREA_WIDTH
        self.board_pixel_height = settings.GAME_AREA_HEIGHT
        # Board top-left corner (board_x, board_y) is now dynamically updated
        # via settings.GAME_AREA_X/Y before drawing/handling clicks.

    def _place_mines(self, first_click_row, first_click_col):
        """
        Places mines randomly on the board, avoiding the first clicked cell
        and its immediate neighbours.
        """
        self.mines_location.clear()
        safe_zone = set()
        # Add first click and neighbours to safe zone
        for r_offset in range(-1, 2):
            for c_offset in range(-1, 2):
                nr, nc = first_click_row + r_offset, first_click_col + c_offset
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    safe_zone.add((nr, nc))

        placed_mines = 0
        # Ensure we don't try to place more mines than available safe cells
        max_possible_mines = (self.rows * self.cols) - len(safe_zone)
        mines_to_place = min(self.mines, max_possible_mines)
        if mines_to_place < self.mines:
            print(f"Warning: Not enough space for {self.mines} mines, placing {mines_to_place}.")


        while placed_mines < mines_to_place:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            if (row, col) not in self.mines_location and (row, col) not in safe_zone:
                self.mines_location.add((row, col))
                self.grid[row][col] = settings.MINE_VALUE # Use MINE_VALUE constant
                placed_mines += 1
        # Update actual mine count if it was reduced
        self.mines = mines_to_place

    def _calculate_adjacent_mines(self):
        """Calculates the number of adjacent mines for each non-mine cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] != settings.MINE_VALUE:
                    count = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            nr, nc = r + i, c + j
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if self.grid[nr][nc] == settings.MINE_VALUE:
                                    count += 1
                    self.grid[r][c] = count

    def handle_click(self, mouse_pos, button):
        """
        Handles a mouse click on the board. Uses current board position from settings.

        Args:
            mouse_pos (tuple): The (x, y) coordinates of the mouse click relative to the window.
            button (int): The mouse button clicked (1 for left, 3 for right).
        """
        if self.game_over or self.game_won:
            return # Don't process clicks if game is finished

        # Use current board top-left from settings for coordinate conversion
        board_x = settings.GAME_AREA_X
        board_y = settings.GAME_AREA_Y

        # Convert window pixel coordinates to grid coordinates
        col = (mouse_pos[0] - board_x) // self.cell_size
        row = (mouse_pos[1] - board_y) // self.cell_size

        # Check if click is within the grid boundaries
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        if button == 1: # Left click
            # Handle first click separately to place mines
            if self.first_click:
                self._place_mines(row, col)
                self._calculate_adjacent_mines()
                self.first_click = False

            # Only reveal if not flagged
            if self.cell_states[row][col] != CellState.FLAGGED:
                self.reveal(row, col)

        elif button == 3: # Right click
            # Only toggle flag if not already revealed
            if self.cell_states[row][col] != CellState.REVEALED:
                self.toggle_flag(row, col)

        # Check for win condition after every valid click that wasn't game over
        if not self.game_over:
            self._check_win()


    def reveal(self, row, col):
        """
        Reveals a cell. If it's a mine, game over. If empty, reveals neighbours.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.
        """
        # Ignore if already revealed or flagged, or if game is over
        # Note: Flag check moved to handle_click to prevent revealing flagged cells
        if self.game_over or self.cell_states[row][col] == CellState.REVEALED:
            return

        # Reveal the cell
        self.cell_states[row][col] = CellState.REVEALED

        # Check if it's a mine
        if self.grid[row][col] == settings.MINE_VALUE:
            self.game_over = True
            self._reveal_all_mines()
            print("Game Over!") # For debugging
            return

        # If it's an empty cell (0 adjacent mines), reveal neighbours recursively
        if self.grid[row][col] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    nr, nc = row + i, col + j
                    # Check bounds and if the neighbour is hidden (not revealed or flagged)
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and \
                       self.cell_states[nr][nc] == CellState.HIDDEN:
                        self.reveal(nr, nc) # Recursive call


    def toggle_flag(self, row, col):
        """
        Toggles a flag on a hidden cell.

        Args:
            row (int): Row index of the cell.
            col (int): Column index of the cell.
        """
         # Already checked in handle_click that cell is not revealed
        if self.cell_states[row][col] == CellState.HIDDEN:
            # Add flag only if flag limit not reached (optional, but common)
            # if self.flags_placed < self.mines:
            self.cell_states[row][col] = CellState.FLAGGED
            self.flags_placed += 1
        elif self.cell_states[row][col] == CellState.FLAGGED:
            self.cell_states[row][col] = CellState.HIDDEN
            self.flags_placed -= 1


    def _reveal_all_mines(self):
        """Reveals all mine locations when the game is over."""
        for r in range(self.rows):
            for c in range(self.cols):
                # Reveal mines that weren't flagged
                if self.grid[r][c] == settings.MINE_VALUE and self.cell_states[r][c] != CellState.FLAGGED:
                    self.cell_states[r][c] = CellState.REVEALED
                # Mark incorrectly placed flags (optional visualization)
                elif self.grid[r][c] != settings.MINE_VALUE and self.cell_states[r][c] == CellState.FLAGGED:
                    # We can add a specific visual indicator later if needed
                    pass


    def _check_win(self):
        """Checks if the player has won the game."""
        revealed_count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                # Win if all non-mine cells are revealed
                if self.cell_states[r][c] == CellState.REVEALED and self.grid[r][c] != settings.MINE_VALUE:
                    revealed_count += 1

        # Total non-mine cells = total cells - number of mines
        total_non_mines = (self.rows * self.cols) - self.mines
        if revealed_count == total_non_mines:
            self.game_won = True
            self.game_over = True # Set game_over to stop further interaction
            # Flag remaining mines automatically (optional nice touch)
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == settings.MINE_VALUE and self.cell_states[r][c] == CellState.HIDDEN:
                        self.cell_states[r][c] = CellState.FLAGGED
                        self.flags_placed += 1
            print("You Won!") # For debugging


    def draw(self, surface):
        """Draws the entire Minesweeper board onto the given surface. Uses current board position."""
        mouse_pos = pygame.mouse.get_pos()
        # Get current board top-left from settings
        board_x = settings.GAME_AREA_X
        board_y = settings.GAME_AREA_Y

        for r in range(self.rows):
            for c in range(self.cols):
                # Calculate cell rect relative to board_x, board_y
                cell_rect = pygame.Rect(
                    board_x + c * self.cell_size,
                    board_y + r * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                # Determine cell colour based on state and theme
                cell_colour = settings.THEME["cell_hidden"]
                draw_content = None # Content to draw inside the cell (text, flag, mine)
                content_colour = settings.THEME["text"] # Default

                # Check for hover, but only on hidden cells and if game not over
                is_hovered = cell_rect.collidepoint(mouse_pos) and \
                             self.cell_states[r][c] == CellState.HIDDEN and \
                             not self.game_over

                if self.cell_states[r][c] == CellState.HIDDEN:
                    cell_colour = settings.THEME["cell_hover"] if is_hovered else settings.THEME["cell_hidden"]
                elif self.cell_states[r][c] == CellState.REVEALED:
                    cell_colour = settings.THEME["cell_revealed"]
                    if self.grid[r][c] == settings.MINE_VALUE:
                        # Draw mine symbol (e.g., circle or 'M')
                        mine_center = cell_rect.center
                        mine_radius = self.cell_size // 4
                        pygame.draw.circle(surface, settings.THEME["mine"], mine_center, mine_radius)
                        # Optionally add background highlight for the hit mine
                        if self.game_over: # Highlight the specific mine clicked
                             pygame.draw.rect(surface, (255, 100, 100), cell_rect, 3) # Red border
                    elif self.grid[r][c] > 0:
                        draw_content = str(self.grid[r][c])
                        # Get number colour from theme, default to black if not found
                        content_colour = settings.THEME["numbers"].get(self.grid[r][c], settings.BLACK)
                    # Else: revealed empty cell, no content needed
                elif self.cell_states[r][c] == CellState.FLAGGED:
                    cell_colour = settings.THEME["cell_hidden"] # Keep hidden colour
                    # Draw flag symbol (e.g., triangle or 'F')
                    flag_points = [
                        (cell_rect.left + self.cell_size * 0.2, cell_rect.top + self.cell_size * 0.2),
                        (cell_rect.left + self.cell_size * 0.8, cell_rect.top + self.cell_size * 0.4),
                        (cell_rect.left + self.cell_size * 0.2, cell_rect.top + self.cell_size * 0.6)
                    ]
                    pygame.draw.polygon(surface, settings.THEME["flag"], flag_points)
                    # Draw pole
                    pygame.draw.line(surface, settings.THEME["flag"],
                                     (cell_rect.centerx, cell_rect.top + self.cell_size * 0.2),
                                     (cell_rect.centerx, cell_rect.bottom - self.cell_size * 0.2), 2)


                # Draw the cell background (unless it's a revealed mine, which draws its own symbol)
                if not (self.cell_states[r][c] == CellState.REVEALED and self.grid[r][c] == settings.MINE_VALUE):
                     pygame.draw.rect(surface, cell_colour, cell_rect)

                # Draw the content (number) if any
                if draw_content:
                    text_surf = settings.FONT_CELL.render(draw_content, True, content_colour)
                    text_rect = text_surf.get_rect(center=cell_rect.center)
                    surface.blit(text_surf, text_rect)

                # Draw grid lines
                pygame.draw.rect(surface, settings.THEME["grid_lines"], cell_rect, 1) # 1px border

        # Draw remaining flags/mines count (position relative to board)
        remaining_mines = self.mines - self.flags_placed
        info_text = f"Mines: {remaining_mines}"
        # Position above the top-right corner of the board
        ui.draw_text(surface, info_text, settings.FONT_SMALL, settings.THEME["text"],
                     board_x + self.board_pixel_width - 5, board_y - 20, center=False).right = board_x + self.board_pixel_width - 5


    def reset(self):
        """Resets the board to its initial state for a new game."""
        # Re-read settings in case grid size/mines changed (though not implemented yet)
        self.rows = settings.GRID_ROWS
        self.cols = settings.GRID_COLS
        self.mines = settings.NUM_MINES

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.cell_states = [[CellState.HIDDEN for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags_placed = 0
        self.mines_location.clear()
        self.first_click = True
        self.game_over = False
        self.game_won = False
        print("Board Reset") # For debugging
