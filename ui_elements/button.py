import pygame
from pygame.font import Font


class Button:
    def __init__(
        self,
        window: pygame.Surface,
        position_x: int,
        position_y: int,
        text: str,
        text_color: str,
        color: str,
        font: Font,
    ):
        self.window = window
        self.color = color

        self.text = font.render(text, True, text_color)
        self.text_rectangle = self.text.get_rect(center=(position_x, position_y))

        button_width = int(self.text_rectangle.width * 1.1)
        button_height = int(self.text_rectangle.height * 1.1)
        self.rectangle = pygame.Rect(
            position_x - button_width // 2,
            position_y - button_height // 2,
            button_width,
            button_height,
        )

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rectangle)
        self.window.blit(self.text, self.text_rectangle)
