from dataclasses import dataclass
from typing import Optional

import pygame
import utils
from constants import Color, Coordinate
from pygame import Surface


@dataclass
class Button:
    """Class used for creating buttons."""

    x: int
    y: int
    width: int
    height: int
    text: Optional[str] = None
    bg_main_color: Color = (0, 0, 0)
    bg_accent_color: Optional[Color] = None
    text_main_color: Color = (255, 255, 255)
    text_accent_color: Optional[Color] = None
    font_name: str = "comicsans"

    def __post_init__(self):
        print("Hello")
        self.hovering = False

        self.render(self.width, self.height, self.x, self.y)
        del self.x, self.y, self.width, self.height

    def render(self, width: int, height: int, x: int, y: int):
        """Render the button.
        This function is meant to be called whenever the window is resized."""
        self.background_surface = pygame.Surface((width, height))
        self.background_rect = self.background_surface.get_rect(center=(x, y))

        self.background_surface.fill(self.bg_main_color)

        self.render_text(width, height)

    def render_text(self, width: int, height: int):
        """Render the button text"""
        if self.text is None:
            return

        maximum_width, maximum_height = int(width * 0.9), int(height * 0.9)
        font_size = utils.get_dynanimc_font_size(
            self.font_name, self.text, maximum_width, maximum_height
        )

        self.font = pygame.font.SysFont(self.font_name, font_size)  #

        text_surface = self.font.render(self.text, True, self.text_main_color)
        self.text_rect = text_surface.get_rect(center=(width // 2, height // 2))

        self.background_surface.blit(text_surface, self.text_rect)

    def check_hover(self, mouse_pos: Coordinate) -> bool:
        """Handle what happens if user hovers over the button.
        Returns wether the state of the button changed"""
        if self.background_rect.collidepoint(*mouse_pos):
            if self.hovering:
                return False

            if self.bg_accent_color is not None:
                self.background_surface.fill(self.bg_accent_color)

            if self.text is not None:
                if self.text_accent_color is not None:
                    text_surface = self.font.render(
                        self.text, True, self.text_accent_color
                    )
                else:
                    text_surface = self.font.render(
                        self.text, True, self.text_main_color
                    )
                self.background_surface.blit(text_surface, self.text_rect)

            self.hovering = True
            return True

        if not self.hovering:
            return False

        if self.bg_accent_color is not None:
            self.background_surface.fill(self.bg_main_color)

            if self.text is not None:
                text_surface = self.font.render(self.text, True, self.text_main_color)
                self.background_surface.blit(text_surface, self.text_rect)

        self.hovering = False
        return True

    def check_press(self):
        """Check if the button was pressed."""
        return self.hovering

    def draw(self, surface: Surface):
        """Draw the button."""
        surface.blit(self.background_surface, self.background_rect)
