import pygame

from src.button import Button
from src.single_player import SinglePlayer


class Mode:
    def __init__(self, screen, font, main_background, menu):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu

    def draw(self):
        easy_mode = Button((290, 150), 230, 50, 'Easy', '#063B14', '#05310E', '#FFFFFF', self.font)
        midle_mode = Button((290, 250), 230, 50, 'Midle', '#52570A', '#444703', '#FFFFFF', self.font)
        hard_mode = Button((290, 350), 230, 50, 'Hard', '#3D0606', '#350505', '#FFFFFF', self.font)
        back = Button((290, 450), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                easy_mode.click(event, lambda:(
                    SinglePlayer(self.screen, self.font, self.main_background, self.menu, (3, 3)).draw()
                ))
                midle_mode.click(event, lambda: (
                    SinglePlayer(self.screen, self.font, self.main_background, self.menu, (4, 4)).draw()
                ))
                hard_mode.click(event, lambda: (
                    SinglePlayer(self.screen, self.font, self.main_background, self.menu, (5, 5)).draw()
                ))

                back.click(event, lambda: (
                    self.menu.draw()
                ))

            easy_mode.draw(self.screen)
            midle_mode.draw(self.screen)
            hard_mode.draw(self.screen)
            back.draw(self.screen)
