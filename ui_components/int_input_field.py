from typing import Optional

import pygame
import util
from constants import Color


class IntInputField:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        min_int: int,
        max_int: int,
        default_text: str,
        border_passive: Color,
        border_active: Color,
        text_color: Color,
        default_text_color: Color,
        start_value: int,
        font_name: str = "comicsans",
    ):
        self.x, self.y = x, y
        self.width, height = width, height
        self.min_int, self.max_int = min_int, max_int
        self.default_text = default_text
        self.border_passive, self.border_active = border_passive, border_active
        self.text_color, self.default_text_color = text_color, default_text_color
        self.font_name = font_name

        self.selected = False
        self.value = start_value
        self.text = str(start_value)

        self.render(x, y, width, height)

    def render(self, x: int, y: int, width: int, height: int):
        self.x, self.y = x, y
        self.width, self.height = width, height

        self.input_rect = pygame.Rect(x, y, width, height)

        self.text_width, self.text_height = int(width * 0.995), int(height * 0.995)

        default_text_font_size = util.get_dynanimc_font_size(
            self.font_name, self.default_text, self.text_width, self.text_height
        )
        default_text_font = pygame.font.SysFont(self.font_name, default_text_font_size)
        self.default_text_surface = default_text_font.render(
            self.default_text, True, self.default_text_color
        )
        self.default_text_rect = self.default_text_surface.get_rect(
            center=self.input_rect.center
        )

        self.text_surface = self.default_text_surface
        self.text_rect = self.default_text_rect

    def render_text(self):
        text_font_size = util.get_dynanimc_font_size(
            self.font_name, self.text, self.text_width, self.text_height
        )
        text_font = pygame.font.SysFont(self.font_name, text_font_size)
        text_surface = text_font.render(self.text, True, self.text_color)
        text_rect = self.text_surface.get_rect(
            center=(
                self.input_rect.centerx,
                self.input_rect.centery,
            )
        )

        return text_surface, text_rect

    def update(self, actions):
        was_selected = self.selected

        if actions["mouse_clicked"]:
            self.selected = self.input_rect.collidepoint(pygame.mouse.get_pos())

        if not was_selected and self.selected:
            self.text = ""

        if actions["enter_pressed"]:
            self.selected = False

        if not self.selected:
            if was_selected:
                if self.text:
                    self.value = min(self.max_int, max(self.min_int, int(self.text)))
                self.text = str(self.value)
        else:
            for letter in actions["keys_pressed"]:
                if letter == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                if letter in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                    self.text += letter

        if self.text:
            self.text_surface, self.text_rect = self.render_text()
        else:
            self.text_surface, self.text_rect = (
                self.default_text_surface,
                self.default_text_rect,
            )

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.text = str(value)

    def draw(self, surface):
        border_color = self.border_active if self.selected else self.border_passive
        pygame.draw.rect(surface, border_color, self.input_rect, 2)

        surface.blit(self.text_surface, self.text_rect)
