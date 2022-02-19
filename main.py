import sys

import pygame

from ui_components.button import Button

pygame.font.init()

window = pygame.display.set_mode((800, 600))
window.fill((255, 255, 255))
button = Button(
    400, 300, 200, 100, "Start Game", (0, 0, 0), (80, 80, 80), (255, 255, 255)
)


# Button()

button.draw(window)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_f:
                button.render(300, 200, 400, 300)
                button.draw(window)
                pygame.display.update()
        if event.type == pygame.MOUSEMOTION:
            if button.check_hover(pygame.mouse.get_pos()):
                button.draw(window)
                pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button.check_press():
                print("Button Clicked!")
