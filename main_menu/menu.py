import sys

import pygame
from application import constants
from application.settings import Settings
from application.window import ApplicationWindow
from ui_elements.button import Button


class MainMenu:
    def __init__(self, settings: Settings, window: ApplicationWindow):
        self.settings = settings
        self.window = window

        self.window.rename("Hangman: Main Menu")

        self.start_button = Button(
            self.window.window,
            400,
            300,
            "Start Game",
            (255, 255, 255),
            (0, 0, 0),
            constants.FONTS["Medium Arial Font"],
        )

    def draw(self):
        background_color_name = self.settings.get("mainMenuBackgroundColor")
        background_color = constants.COLORS[background_color_name]
        self.window.fill(background_color)
        self.start_button.draw()
        pygame.display.update()

    def start(self):
        self.draw()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
