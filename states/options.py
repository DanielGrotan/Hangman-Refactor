import constants
import pygame
import util
from ui_components.button import Button
from ui_components.int_input_field import IntInputField

from .state import State


class Options(State):
    def __init__(self, game):
        super().__init__(game)

        screen_width = self.game.screen_width
        screen_height = self.game.screen_height

        title_font_size = util.get_dynanimc_font_size(
            "comicsans", "Options", screen_width // 6, screen_height // 9
        )
        title_font = pygame.font.SysFont("comicsans", title_font_size)

        self.title_surf = title_font.render("Options", True, constants.WHITE)
        self.title_rect = self.title_surf.get_rect(midtop=(screen_width // 2, 0))

        self.screen_width_field = IntInputField(
            screen_width // 6 * 3,
            screen_height // 9 * 2,
            screen_width // 3,
            screen_height // 9,
            400,
            self.game.monitor_width,
            "Enter Screen Width",
            constants.BLUE,
            constants.GREEN,
            constants.WHITE,
            constants.GREY,
            screen_width,
        )

        text_font_size = util.get_dynanimc_font_size(
            "comicsans", "Screen Width: ", screen_width // 3, screen_height // 9
        )
        text_font = pygame.font.SysFont("comicsans", text_font_size)

        text_x_position = screen_width // 6

        self.screen_width_text_surf = text_font.render(
            "Screen Width: ", True, constants.WHITE
        )
        self.screen_width_text_rect = self.screen_width_text_surf.get_rect(
            midleft=(text_x_position, screen_height // 9 * 2 + screen_height // 18)
        )

        self.screen_height_field = IntInputField(
            screen_width // 6 * 3,
            screen_height // 9 * 4,
            screen_width // 3,
            screen_height // 9,
            400,
            self.game.monitor_height,
            "Enter Screen Height",
            constants.BLUE,
            constants.GREEN,
            constants.WHITE,
            constants.GREY,
            screen_height,
        )

        self.screen_height_text_surf = text_font.render(
            "Screen Height: ", True, constants.WHITE
        )
        self.screen_height_text_rect = self.screen_width_text_surf.get_rect(
            midleft=(text_x_position, screen_height // 9 * 4 + screen_height // 18)
        )

        button_width = screen_width // 6
        button_height = screen_height // 9

        self.fullscreen_button = Button(
            button_width // 2,
            screen_height // 9 * 7 - button_height // 2,
            button_width,
            button_height,
            "Fullscreen",
            constants.WHITE,
            constants.GREY,
            constants.BLACK,
        )

        self.apply_button = Button(
            screen_width // 2 - button_width // 2 - int(button_width * 0.1),
            screen_height // 9 * 8 - button_height // 2,
            button_width,
            button_height,
            "Apply",
            constants.WHITE,
            constants.GREY,
            constants.BLACK,
        )

        self.back_button = Button(
            screen_width // 2 + button_width // 2 + int(button_width * 0.1),
            screen_height // 9 * 8 - button_height // 2,
            button_width,
            button_height,
            "Back",
            constants.WHITE,
            constants.GREY,
            constants.BLACK,
        )

    def on_resize(self, new_width, new_height):
        title_font_size = util.get_dynanimc_font_size(
            "comicsans", "Options", new_width // 6, new_height // 9
        )
        title_font = pygame.font.SysFont("comicsans", title_font_size)

        self.title_surf = title_font.render("Options", True, constants.WHITE)
        self.title_rect = self.title_surf.get_rect(midtop=(new_width // 2, 0))

        self.screen_width_field.render(
            new_width // 6 * 3,
            new_height // 9 * 2,
            new_width // 3,
            new_height // 9,
        )

        text_font_size = util.get_dynanimc_font_size(
            "comicsans", "Screen Width: ", new_width // 3, new_height // 9
        )
        text_font = pygame.font.SysFont("comicsans", text_font_size)

        text_x_position = new_width // 6

        self.screen_width_text_surf = text_font.render(
            "Screen Width: ", True, constants.WHITE
        )
        self.screen_width_text_rect = self.screen_width_text_surf.get_rect(
            midleft=(text_x_position, new_height // 9 * 2 + new_height // 18)
        )

        self.screen_height_field.render(
            new_width // 6 * 3,
            new_height // 9 * 4,
            new_width // 3,
            new_height // 9,
        )

        self.screen_height_text_surf = text_font.render(
            "Screen Height: ", True, constants.WHITE
        )
        self.screen_height_text_rect = self.screen_width_text_surf.get_rect(
            midleft=(text_x_position, new_height // 9 * 4 + new_height // 18)
        )

        self.screen_width_field.set_value(new_width)
        self.screen_height_field.set_value(new_height)

        self.fullscreen_button.render(
            new_width // 6,
            new_height // 9,
            new_width // 12,
            new_height // 9 * 7 - new_height // 18,
        )

        self.apply_button.render(
            new_width // 12,
            new_height // 9,
            new_width // 2 - new_width // 24 - int(new_width // 12 * 0.1),
            new_height // 9 * 8 - new_height // 18,
        )

        self.back_button.render(
            new_width // 12,
            new_height // 9,
            new_width // 2 + new_width // 24 + int(new_width // 12 * 0.1),
            new_height // 9 * 8 - new_height // 18,
        )

    def update(self, _, actions):
        self.screen_width_field.update(actions)
        self.screen_height_field.update(actions)

        if actions["mouse_moved"]:
            mouse_pos = pygame.mouse.get_pos()
            self.fullscreen_button.check_hover(mouse_pos)
            self.apply_button.check_hover(mouse_pos)
            self.back_button.check_hover(mouse_pos)

        if actions["mouse_clicked"]:
            if self.fullscreen_button.check_press():
                self.screen_width_field.set_value(self.game.monitor_width)
                self.screen_height_field.set_value(self.game.monitor_height)
            if self.apply_button.check_press():
                screen_width_value = self.screen_width_field.get_value()
                screen_height_value = self.screen_height_field.get_value()

                if screen_width_value != self.game.screen_width:
                    self.game.resize(screen_width_value, screen_height_value)
                elif screen_height_value != self.game.screen_height:
                    self.game.resize(screen_width_value, screen_height_value)
            elif self.back_button.check_press():
                self.exit_state()

    def render(self, surface):
        surface.fill(constants.BLACK)

        surface.blit(self.title_surf, self.title_rect)

        self.screen_width_field.draw(surface)
        surface.blit(self.screen_width_text_surf, self.screen_width_text_rect)

        self.screen_height_field.draw(surface)
        surface.blit(self.screen_height_text_surf, self.screen_height_text_rect)

        self.fullscreen_button.draw(surface)

        self.apply_button.draw(surface)
        self.back_button.draw(surface)

    def enter_state(self):
        super().enter_state()
        pygame.display.set_caption("Hangman: Options")

    def exit_state(self):
        super().exit_state()
        pygame.display.set_caption("Hangman: Main Menu")
