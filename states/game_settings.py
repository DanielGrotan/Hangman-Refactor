import math

import constants
import pygame
import util
from ui_components.button import Button
from ui_components.int_input_field import IntInputField

from .state import State


class GameSettings(State):
    def __init__(self, game):
        super().__init__(game)

        self.enter_state()

        screen_width, screen_height = game.screen_width, game.screen_height

        self.render_objects(screen_width, screen_height)
        self.render_buttons(screen_width, screen_height)

        self.lives_input_field = IntInputField(
            screen_width // 9 * 7,
            screen_height // 9 * 2,
            screen_width // 9 * 2,
            screen_height // 9,
            7,
            26,
            "Enter the maximum amount of lives",
            constants.BLUE,
            constants.GREEN,
            constants.WHITE,
            constants.GREY,
            self.previous_state.max_lives,
        )

        self.min_letters_input_field = IntInputField(
            screen_width // 9 * 7,
            screen_height // 9 * 3,
            screen_width // 9 * 2,
            screen_height // 9,
            2,
            math.inf,
            "Enter the lowest amount of letters",
            constants.BLUE,
            constants.GREEN,
            constants.WHITE,
            constants.GREY,
            self.previous_state.min_letters,
        )

        self.max_letters_input_field = IntInputField(
            screen_width // 9 * 7,
            screen_height // 9 * 4,
            screen_width // 9 * 2,
            screen_height // 9,
            2,
            math.inf,
            "Enter the highest amount of letters",
            constants.BLUE,
            constants.GREEN,
            constants.WHITE,
            constants.GREY,
            self.previous_state.max_letters,
        )

    def render_objects(self, new_width, new_height):
        self.surface = pygame.Surface((new_width // 3, new_height))
        self.surface_rect = self.surface.get_rect(topright=(new_width, 0))

        title = "Game Settings"
        font_size = util.get_dynanimc_font_size(
            "comicsans", title, new_width // 3, new_height // 9
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.title_surf = font.render(title, True, constants.WHITE)
        self.title_rect = self.title_surf.get_rect(midtop=(new_width // 6, 0))

        text = " Max Lives: "
        font_size = util.get_dynanimc_font_size(
            "comicsans", text, new_width // 9, new_height // 9
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.max_lives_surf = font.render(text, True, constants.WHITE)
        self.max_lives_rect = self.max_lives_surf.get_rect(
            midleft=(0, new_height // 9 * 3 - new_height // 18)
        )

        text = " Min Letters: "
        font_size = util.get_dynanimc_font_size(
            "comicsans", text, new_width // 9, new_height // 9
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.min_letters_surf = font.render(text, True, constants.WHITE)
        self.min_letters_rect = self.max_lives_surf.get_rect(
            midleft=(0, new_height // 9 * 4 - new_height // 18)
        )

        text = " Max Letters: "
        font_size = util.get_dynanimc_font_size(
            "comicsans", text, new_width // 9, new_height // 9
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.max_letters_surf = font.render(text, True, constants.WHITE)
        self.max_letters_rect = self.max_lives_surf.get_rect(
            midleft=(0, new_height // 9 * 5 - new_height // 18)
        )

    def render_buttons(self, new_width, new_height):
        button_width = new_width // 9
        button_height = new_height // 9

        self.restart_button = Button(
            new_width // 9 * 7 - int(button_width * 0.05),
            new_height // 9 * 8 - button_height // 2,
            button_width,
            button_height,
            "Restart",
            constants.WHITE,
            constants.GREY,
            constants.BLACK,
        )

        self.main_menu_button = Button(
            new_width // 9 * 8 + int(button_width * 0.05),
            new_height // 9 * 8 - button_height // 2,
            button_width,
            button_height,
            "Main Menu",
            constants.WHITE,
            constants.GREY,
            constants.BLACK,
        )

    def on_resize(self, new_width, new_height):
        self.render_objects(new_width, new_height)
        self.render_buttons(new_width, new_height)

        self.lives_input_field.render(
            new_width // 9 * 7,
            new_height // 9 * 2,
            new_width // 9 * 2,
            new_height // 9,
        )

        self.min_letters_input_field.render(
            new_width // 9 * 7,
            new_height // 9 * 3,
            new_width // 9 * 2,
            new_height // 9,
        )

        self.max_letters_input_field.render(
            new_width // 9 * 7,
            new_height // 9 * 4,
            new_width // 9 * 2,
            new_height // 9,
        )

    def update(self, delta_time, actions):
        if actions["escape_pressed"]:
            self.exit_state()

        if actions["mouse_moved"]:
            mouse_pos = pygame.mouse.get_pos()
            self.restart_button.check_hover(mouse_pos)
            self.main_menu_button.check_hover(mouse_pos)

        if actions["mouse_clicked"]:
            if self.restart_button.check_press():
                self.exit_state()
                self.previous_state.setup()
            elif self.main_menu_button.check_press():
                self.exit_state()
                self.previous_state.exit_state()

        self.lives_input_field.update(actions)
        self.min_letters_input_field.update(actions)
        self.max_letters_input_field.update(actions)

        max_letters = self.max_letters_input_field.get_value()
        if max_letters < self.min_letters_input_field.get_value():
            self.min_letters_input_field.set_value(max_letters)

    def render(self, surface):
        self.previous_state.render(surface)

        self.surface.blit(self.title_surf, self.title_rect)
        self.surface.blit(self.max_lives_surf, self.max_lives_rect)
        self.surface.blit(self.min_letters_surf, self.min_letters_rect)
        self.surface.blit(self.max_letters_surf, self.max_letters_rect)

        surface.blit(self.surface, self.surface_rect)

        self.lives_input_field.draw(surface)
        self.min_letters_input_field.draw(surface)
        self.max_letters_input_field.draw(surface)

        self.restart_button.draw(surface)
        self.main_menu_button.draw(surface)

    def exit_state(self):
        self.previous_state.max_lives = self.lives_input_field.get_value()
        self.previous_state.min_letters = self.min_letters_input_field.get_value()
        self.previous_state.max_letters = self.max_letters_input_field.get_value()

        super().exit_state()
