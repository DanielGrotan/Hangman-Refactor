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

        background_color_name = self.settings.get("mainMenuBackgroundColor")
        self.background_color = constants.COLORS[background_color_name]

        self.create_buttons(self.window.screen_width, self.window.screen_height)

    def create_buttons(self, screen_width, screen_height):
        self.start_button = Button(
            self.window.window,
            screen_width // 2,
            screen_height // 10 * 2,
            screen_width // 3,
            screen_height // 5,
            self.settings.get("mainMenuButtonFontSize"),
            self.settings.get("mainMenuButtonFont"),
            "Start Game",
            self.settings.get("mainMenuButtonTextColor"),
            self.settings.get("mainMenuButtonColor"),
        )
        self.options_button = Button(
            self.window.window,
            screen_width // 2,
            screen_height // 10 * 5,
            screen_width // 3,
            screen_height // 5,
            self.settings.get("mainMenuButtonFontSize"),
            self.settings.get("mainMenuButtonFont"),
            "Options",
            self.settings.get("mainMenuButtonTextColor"),
            self.settings.get("mainMenuButtonColor"),
        )
        self.quit_button = Button(
            self.window.window,
            screen_width // 2,
            screen_height // 10 * 8,
            screen_width // 3,
            screen_height // 5,
            self.settings.get("mainMenuButtonFontSize"),
            self.settings.get("mainMenuButtonFont"),
            "Quit Game",
            self.settings.get("mainMenuButtonTextColor"),
            self.settings.get("mainMenuButtonColor"),
        )

    def draw(self):
        self.window.fill(self.background_color)
        self.start_button.draw()
        self.options_button.draw()
        self.quit_button.draw()
        pygame.display.update()

    def start(self):
        self.draw()

        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.quit_button.check_press(pygame.mouse.get_pos()):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.window.resize(event.w, event.h)
                    self.create_buttons(event.w, event.h)
                    self.draw()
