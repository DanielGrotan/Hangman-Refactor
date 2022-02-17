import pygame

from .settings import Settings


class ApplicationWindow:
    def __init__(self, settings: Settings, application_name: str):
        self.settings = settings
        self.rename(application_name)
        self.resize(*settings.get("selectedScreenSize"))

    def rename(self, new_name: str):
        self.application_name = new_name
        pygame.display.set_caption(self.application_name)

    def resize(self, new_width: int, new_height: int):
        self.screen_width, self.screen_height = new_width, new_height
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )

        self.settings.modify("selectedScreenSize", [new_width, new_height])

        self.blit = self.window.blit
        self.fill = self.window.fill
