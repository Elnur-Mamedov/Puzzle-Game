import pygame
import sys

from src.Models.button import Button
from src.Views.mode import Mode
from src.Views.records import Records
from src.Views.settings import Settings


class Menu:
    def __init__(self, screen, font, main_background):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.sound = True

    def draw(self, sound=None):
        if sound is not None:
            if sound:
                self.sound = sound
            else:
                self.sound = sound

        if self.sound:
            click_sound = '../assets/Sounds/Buttonclick.wav'
        else:
            click_sound = None

        new_game = Button((290, 100), 230, 50, 'New game', '#38083B', '#2D032D', '#FFFFFF', self.font,
                          click_sound)

        multiplayer = Button((290, 200), 230, 50, 'Multiplayer', '#38083B', '#2D032D', '#FFFFFF', self.font,
                             click_sound)

        records = Button((290, 300), 230, 50, 'Records', '#38083B', '#2D032D', '#FFFFFF', self.font,
                          click_sound)

        settings = Button((290, 400), 230, 50, 'Settings', '#38083B', '#2D032D', '#FFFFFF', self.font,
                          click_sound)

        exit = Button((290, 530), 230, 50, 'Exit', '#3D0606', '#350505', '#FFFFFF', self.font)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                new_game.click(event, lambda: (
                    Mode(self.screen, self.font, self.main_background, self, 'Single', click_sound).draw()
                ))

                multiplayer.click(event, lambda: (
                    Mode(self.screen, self.font, self.main_background, self, 'Multiplayer', click_sound).draw()
                ))

                records.click(event, lambda: (
                    Records("Statistics.json", self.screen, self.font, self).draw()
                ))

                settings.click(event, lambda:(
                    Settings(self.screen, self.font, self.main_background, self, click_sound).draw()
                ))

                exit.click(event, lambda: (
                    pygame.quit(),
                    sys.exit()
                ))

            new_game.draw(self.screen)
            multiplayer.draw(self.screen)
            settings.draw(self.screen)
            exit.draw(self.screen)
            records.draw(self.screen)
