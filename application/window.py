import ctypes

import pygame

from .settings import Settings


class ApplicationWindow:
    def __init__(self, settings: Settings, application_name: str):
        self.settings = settings

        user32 = ctypes.windll.user32

        self.max_screen_width = user32.GetSystemMetrics(0)
        self.max_screen_height = user32.GetSystemMetrics(1)

        self.rename(application_name)
        self.resize(*settings.get("selectedScreenSize"))

    def rename(self, new_name: str):
        self.application_name = new_name
        pygame.display.set_caption(self.application_name)

    def fullscreen(self):
        self.screen_width = self.max_screen_width
        self.screen_height = self.max_screen_height
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.FULLSCREEN
        )

        self.settings.modify(
            "selectedScreenSize", [self.screen_width, self.screen_height]
        )

        self.blit = self.window.blit
        self.fill = self.window.fill

    def resize(self, new_width: int, new_height: int):
        self.screen_width, self.screen_height = new_width, new_height
        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )

        self.settings.modify("selectedScreenSize", [new_width, new_height])

        self.blit = self.window.blit
        self.fill = self.window.fill
