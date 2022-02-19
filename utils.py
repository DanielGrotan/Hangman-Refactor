import pygame

import constants


def get_dynanimc_font_size(
    font_name: str, text: str, maximum_width: int, maximum_height: int
) -> int:
    """Returns a dynamic font size,
    so that the wanted text can be rendered within a specified width and height
    """
    current_font_size = 1
    while True:
        font = pygame.font.SysFont(font_name, current_font_size)
        text_surface = font.render(text, True, constants.BLACK)
        width, height = text_surface.get_width(), text_surface.get_height()

        if width > maximum_width or height > maximum_height:
            return current_font_size - 1

        current_font_size += 1
