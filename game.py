import json
import sys

import pygame

from states.main_menu import MainMenu
from states.options import Options
from states.state import State


class Game:
    def __init__(self):
        pygame.init()

        monitor_info = pygame.display.Info()
        self.monitor_width, self.monitor_height = (
            monitor_info.current_w,
            monitor_info.current_h,
        )

        self.load_settings()
        flag = pygame.FULLSCREEN if self.settings["isFullscreen"] else pygame.RESIZABLE
        self.display = pygame.display.set_mode(
            (self.screen_width, self.screen_height), flag
        )

        self.running, self.quit = True, False
        self.state_stack: list[State] = []
        self.on_resize_callback = []
        self.actions = {
            "mouse_moved": False,
            "mouse_clicked": False,
            "keys_pressed": [],
            "enter_pressed": False,
        }
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.load_states()

    def load_settings(self):
        with open("settings.json") as settings_file:
            self.settings = json.load(settings_file)

        if self.settings["isFullscreen"]:
            self.screen_width, self.screen_height = (
                self.monitor_width,
                self.monitor_height,
            )
            self.settings["screenWidth"] = self.monitor_width
            self.settings["screenHeight"] = self.monitor_height
        else:
            self.screen_width = min(self.settings["screenWidth"], self.monitor_width)
            self.screen_height = min(self.settings["screenHeight"], self.monitor_height)

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file)

    def load_states(self):
        self.main_menu = MainMenu(self)
        self.main_menu.enter_state()

    def resize(self, new_width, new_height):
        fullscreen = (
            new_width == self.monitor_width and new_height == self.monitor_height
        )

        self.settings["isFullscreen"] = fullscreen

        if fullscreen:
            self.screen_width, self.screen_height = (
                self.monitor_width,
                self.monitor_height,
            )
        else:
            self.screen_width = min(new_width, self.monitor_width)
            self.screen_height = min(new_height, self.monitor_height)

        flag = pygame.FULLSCREEN if fullscreen else pygame.RESIZABLE

        self.display = pygame.display.set_mode(
            (self.screen_width, self.screen_height), flag
        )

        self.settings["screenWidth"] = self.screen_width
        self.settings["screenHeight"] = self.screen_height

        for callback in self.on_resize_callback:
            callback(self.screen_width, self.screen_height)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEMOTION:
                self.actions["mouse_moved"] = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.actions["mouse_clicked"] = True
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.actions["keys_pressed"].append(event.key)
                elif event.key == pygame.K_RETURN:
                    self.actions["enter_pressed"] = True
                else:
                    self.actions["keys_pressed"].append(event.unicode)

    def reset_keys(self):
        self.actions = {
            "mouse_moved": False,
            "mouse_clicked": False,
            "keys_pressed": [],
            "enter_pressed": False,
        }

    def quit_game(self):
        self.save_settings()
        pygame.quit()
        sys.exit()

    def update(self, delta_time):
        self.state_stack[-1].update(delta_time, self.actions)

        if self.quit:
            self.quit_game()

        self.reset_keys()

    def render(self):
        self.state_stack[-1].render(self.display)
        pygame.display.update()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.FPS) / 1000
            self.check_events()
            self.update(delta_time)
            self.render()
