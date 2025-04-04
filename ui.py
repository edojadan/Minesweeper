# ui.py
"""
Contains UI helper functions for the Minesweeper game, like creating buttons.
Uses British English spelling (colour).
"""
import pygame
import settings # Import settings to access theme colours and fonts

def draw_text(surface, text, font, colour, x, y, center=False):
    """Draws text onto a surface."""
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
    return text_rect # Return rect for potential click detection

def button(surface, text, x, y, width, height, action=None, font=None, center_text=True):
    """
    Draws a button and handles basic hover/click detection.

    Args:
        surface: The pygame surface to draw on.
        text: The text to display on the button.
        x: The x-coordinate of the top-left corner.
        y: The y-coordinate of the top-left corner.
        width: The width of the button.
        height: The height of the button.
        action: A function to call when the button is clicked.
        font: The pygame font object to use. Defaults to FONT_MEDIUM from settings.
        center_text: Boolean, if True center text horizontally and vertically.

    Returns:
        bool: True if the button was clicked in this frame, False otherwise.
    """
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    clicked_this_frame = False

    button_rect = pygame.Rect(x, y, width, height)
    on_button = button_rect.collidepoint(mouse_pos)

    # Determine colours based on hover state
    bg_colour = settings.THEME["button_hover"] if on_button else settings.THEME["button_bg"]
    text_colour = settings.THEME["button_text"]

    # Use default font if none provided
    if font is None:
        font = settings.FONT_MEDIUM

    # Draw the button rectangle
    pygame.draw.rect(surface, bg_colour, button_rect, border_radius=5)

    # Draw the text
    text_surf = font.render(text, True, text_colour)
    text_rect = text_surf.get_rect()

    if center_text:
        text_rect.center = button_rect.center
    else:
        # Add small padding if not centered
        text_rect.topleft = (x + 5, y + (height - text_rect.height) // 2)

    surface.blit(text_surf, text_rect)

    # Check for click
    if on_button and click[0] == 1 and action is not None:
        action()
        clicked_this_frame = True # Indicate click happened

    return clicked_this_frame # Return status
