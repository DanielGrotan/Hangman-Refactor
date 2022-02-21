import constants
import pygame
from ui_components.button import Button

from .options import Options
from .state import State


class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.create_buttons()

        self.buttons = [self.start_button, self.options_button, self.quit_button]

    def create_buttons(self):
        screen_width = self.game.screen_width
        screen_height = self.game.screen_height

        button_width = screen_width // 3
        button_height = screen_height // 6

        button_bg_main = constants.BLACK
        button_bg_accent = constants.GREY

        text_main = constants.WHITE
        text_accent = constants.BLACK

        self.start_button = Button(
            screen_width // 2,
            screen_height // 12 * 5 - button_height // 2,
            button_width,
            button_height,
            "Start Game",
            button_bg_main,
            button_bg_accent,
            text_main,
            text_accent,
        )

        self.options_button = Button(
            screen_width // 2,
            screen_height // 12 * 8 - button_height // 2,
            button_width,
            button_height,
            "Options",
            button_bg_main,
            button_bg_accent,
            text_main,
            text_accent,
        )

        self.quit_button = Button(
            screen_width // 2,
            screen_height // 12 * 11 - button_height // 2,
            button_width,
            button_height,
            "Quit Game",
            button_bg_main,
            button_bg_accent,
            text_main,
            text_accent,
        )

    def update(self, delta_time, actions):
        if actions["mouse_moved"]:
            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                button.check_hover(mouse_pos)
        if actions["mouse_clicked"]:
            if self.start_button.check_press():
                pass
            elif self.options_button.check_press():
                options_state = Options(self.game)
                options_state.enter_state()
            elif self.quit_button.check_press():
                self.game.quit = True
                self.exit_state()

    def render(self, surface):
        surface.fill(constants.BLACK)
        for button in self.buttons:
            button.draw(surface)

    def on_resize(self, new_width, new_height):
        button_width = new_width // 3
        button_height = new_height // 6

        self.start_button.render(
            button_width,
            button_height,
            new_width // 2,
            new_height // 12 * 5 - button_height // 2,
        )

        self.options_button.render(
            button_width,
            button_height,
            new_width // 2,
            new_height // 12 * 8 - button_height // 2,
        )

        self.quit_button.render(
            button_width,
            button_height,
            new_width // 2,
            new_height // 12 * 11 - button_height // 2,
        )

    def enter_state(self):
        super().enter_state()
        pygame.display.set_caption("Hangman: Main Menu")
