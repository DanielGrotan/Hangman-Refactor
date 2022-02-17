import pygame
from application.types import Color
from pygame.font import Font


class Button:
    def __init__(
        self,
        window: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        font_size: int,
        font_type: str,
        text: str,
        text_color: Color,
        color: Color,
    ):

        self.window = window
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.color = color

        self.surface = pygame.Surface((width, height))
        self.surface_rect = self.surface.get_rect(center=(x, y))

        self.generate_text(font_type, font_size, text, text_color)

    def generate_text(
        self,
        font_type: str,
        font_size: int,
        text: str,
        text_color: Color,
    ):
        while True:
            font = pygame.font.SysFont(font_type, font_size)
            text_render = font.render(text, True, text_color)

            if (
                text_render.get_width() > self.width
                or text_render.get_height() > self.height
            ):
                font_size -= 1
            else:
                self.text = text_render
                self.text_rect = self.text.get_rect(
                    center=(self.width // 2, self.height // 2)
                )
                return

    def draw(self):
        self.surface.fill(self.color)
        self.surface.blit(self.text, self.text_rect)
        self.window.blit(self.surface, self.surface_rect)

    def check_press(self, mouse_position: tuple[int, int]):
        return self.surface_rect.collidepoint(*mouse_position)
