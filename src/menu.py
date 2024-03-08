import pygame
import sys

from src.button import Button
from src.mode import Mode


class Menu:
    def __init__(self, screen, font, main_background):
        self.screen = screen
        self.font = font
        self.main_background = main_background

    def draw(self):
        new_game = Button((290, 150), 230, 50, 'New game', '#38083B', '#2D032D', '#FFFFFF', self.font)
        multiplayer = Button((290, 250), 230, 50, 'Multiplayer', '#38083B', '#2D032D', '#FFFFFF', self.font)
        settings = Button((290, 350), 230, 50, 'Settings', '#38083B', '#2D032D', '#FFFFFF', self.font)
        exit = Button((290, 450), 230, 50, 'Exit', '#3D0606', '#350505', '#FFFFFF', self.font)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                new_game.click(event, lambda: (
                    Mode(self.screen, self.font, self.main_background, self).draw()
                ))

                multiplayer.click(event, lambda: (
                    Mode(self.screen, self.font, self.main_background, self).draw()
                ))

                settings.click(event)

                exit.click(event, lambda: (
                    pygame.quit(),
                    sys.exit()
                ))

            new_game.draw(self.screen)
            multiplayer.draw(self.screen)
            settings.draw(self.screen)
            exit.draw(self.screen)
