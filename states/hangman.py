import math
import os

import constants
import pygame
import util
from ui_components.button import Button

from .state import State


class Hangman(State):
    def __init__(self, game):
        super().__init__(game)
        self.setup()
        self.load_images()

    def load_images(self):
        self.images = []
        base_path = os.path.dirname(__file__).replace("states", "assets")
        for image_index in range(7):
            image = pygame.image.load(
                os.path.join(base_path, f"hangman{image_index}.png")
            )
            image = pygame.transform.scale(
                image, (self.screen_width // 3, self.screen_height // 3)
            )
            self.images.append(image)

    def setup(self):
        self.screen_width, self.screen_height = (
            self.game.screen_width,
            self.game.screen_height,
        )

        self.word = util.get_random_word(1, math.inf)
        self.correct_letters = set(self.word)

        self.lives = max(7, min(26 - len(self.correct_letters), 10))
        self.lives_per_image = self.lives // 7

        self.current_image = 0
        self.wrong = 0

        self.guessed = set()
        self.guessed_ordered = []
        self.progress = ["_" for _ in self.word]

        self.won = False
        self.lost = False

        self.render_lives_text()
        self.render_guessed_letters_text()
        self.render_progress_text()
        self.render_game_over_text()
        self.render_buttons()

    def render_lives_text(self):
        text = f"Lives Remaining: {self.lives - self.wrong}"
        font_size = util.get_dynanimc_font_size(
            "comicsans", text, self.screen_width // 3, self.screen_height // 6
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.lives_text_surf = font.render(text, True, constants.BLACK)
        self.lives_text_rect = self.lives_text_surf.get_rect(
            topright=(self.screen_width, self.screen_height // 3)
        )

    def render_guessed_letters_text(self):
        self.guessed_letters_surf = pygame.Surface(
            (self.screen_width // 3, self.screen_height // 3)
        )
        self.guessed_letters_surf.fill(constants.WHITE)

        self.guessed_letters_rect = self.guessed_letters_surf.get_rect(topleft=(0, 0))

        title_text = "Wrong letters:"
        title_font_size = util.get_dynanimc_font_size(
            "comicsans", title_text, self.screen_width // 3, self.screen_height // 6
        )
        title_font = pygame.font.SysFont("comicsans", title_font_size)
        title_text_surf = title_font.render(title_text, True, constants.BLACK)
        title_text_rect = title_text_surf.get_rect(
            center=(self.screen_width // 6, self.screen_height // 12)
        )
        self.guessed_letters_surf.blit(title_text_surf, title_text_rect)

        guessed_letters_text = " ".join(self.guessed_ordered)
        guessed_letters_font_size = util.get_dynanimc_font_size(
            "comicsans",
            guessed_letters_text,
            self.screen_width // 3,
            self.screen_height // 6,
        )
        guessed_letters_font = pygame.font.SysFont(
            "comicsans", guessed_letters_font_size
        )
        guessed_letters_text_surf = guessed_letters_font.render(
            guessed_letters_text, True, constants.BLACK
        )
        guessed_letters_text_rect = guessed_letters_text_surf.get_rect(
            topleft=(0, self.screen_height // 6)
        )
        self.guessed_letters_surf.blit(
            guessed_letters_text_surf, guessed_letters_text_rect
        )

    def render_progress_text(self):
        progress_text = " ".join(self.progress)
        font_size = util.get_dynanimc_font_size(
            "comicsans", progress_text, self.screen_width, self.screen_height // 4
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.progress_text_surf = font.render(progress_text, True, constants.BLACK)
        self.progress_text_rect = self.progress_text_surf.get_rect(
            midbottom=(self.screen_width // 2, self.screen_height)
        )

    def render_game_over_text(self):
        victory_text = "You guessed every letter of the word correctly!"
        font_size = util.get_dynanimc_font_size(
            "comicsans", victory_text, self.screen_width // 2, self.screen_height // 3
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.victory_text_surf = font.render(victory_text, True, constants.GREEN)
        self.victory_text_rect = self.victory_text_surf.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )

        loss_text = f"You ran out of lives! The word was: {self.word}"
        font_size = util.get_dynanimc_font_size(
            "comicsans", loss_text, self.screen_width // 2, self.screen_height // 3
        )
        font = pygame.font.SysFont("comicsans", font_size)

        self.loss_text_surf = font.render(loss_text, True, constants.RED)
        self.loss_text_rect = self.loss_text_surf.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )

    def render_buttons(self):
        button_width = self.screen_width // 6
        button_height = self.screen_height // 6

        self.restart_button = Button(
            self.screen_width // 2 - button_width // 2 - (self.screen_width // 6 * 0.1),
            self.screen_height // 6 * 4,
            button_width,
            button_height,
            "Restart",
            constants.BLACK,
            constants.GREY,
            constants.WHITE,
        )
        self.main_menu_button = Button(
            self.screen_width // 2 + button_width // 2 + (self.screen_width // 6 * 0.1),
            self.screen_height // 6 * 4,
            button_width,
            button_height,
            "Main Menu",
            constants.BLACK,
            constants.GREY,
            constants.WHITE,
        )

    def on_resize(self, new_width, new_height):
        self.screen_width, self.screen_height = new_width, new_height
        self.render_lives_text()
        self.render_guessed_letters_text()
        self.render_progress_text()
        self.render_game_over_text()
        self.render_buttons()
        self.load_images()

    def check_letter(self, letter):
        if letter in self.guessed or letter not in constants.ALPHABET:
            return False

        self.guessed.add(letter)

        if letter not in self.correct_letters:
            self.wrong += 1
            self.guessed_ordered.append(letter)
            self.render_guessed_letters_text()
            self.render_lives_text()
            return False

        correct = False
        for i, correct_letter in enumerate(self.word):
            if letter == correct_letter:
                self.progress[i] = letter
                correct = True

        return correct

    def update(self, delta_time, actions):
        if actions["mouse_moved"]:
            mouse_pos = pygame.mouse.get_pos()
            self.restart_button.check_hover(mouse_pos)
            self.main_menu_button.check_hover(mouse_pos)

        if self.won or self.lost:
            if actions["mouse_clicked"]:
                if self.restart_button.check_press():
                    self.setup()
                elif self.main_menu_button.check_press():
                    self.exit_state()
            return

        any_correct = False
        for letter in actions["keys_pressed"]:
            correct = self.check_letter(letter)

            if not any_correct:
                any_correct = correct

        if any_correct:
            self.render_progress_text()

        image_index = self.wrong // self.lives_per_image
        if image_index > self.current_image and image_index < 6:
            self.current_image = image_index

        if "_" not in self.progress:
            self.won = True

        if self.wrong == self.lives:
            self.current_image = 6
            self.lost = True
            self.progress = [letter for letter in self.word]
            self.render_progress_text()

    def render(self, surface):
        surface.fill(constants.WHITE)
        surface.blit(
            self.images[self.current_image],
            self.images[self.current_image].get_rect(topright=(self.screen_width, 0)),
        )
        surface.blit(self.lives_text_surf, self.lives_text_rect)
        surface.blit(self.guessed_letters_surf, self.guessed_letters_rect)
        surface.blit(self.progress_text_surf, self.progress_text_rect)

        if self.won:
            surface.blit(self.victory_text_surf, self.victory_text_rect)
        elif self.lost:
            surface.blit(self.loss_text_surf, self.loss_text_rect)

        if self.won or self.lost:
            self.restart_button.draw(surface)
            self.main_menu_button.draw(surface)

    def enter_state(self):
        super().enter_state()
        pygame.display.set_caption("Hangman: Game")

    def exit_state(self):
        super().exit_state()
        pygame.display.set_caption("Hangman: Main Menu")
