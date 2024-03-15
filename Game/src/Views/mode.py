import pygame

from src.Models.button import Button
from src.Views.multiplayer import Multiplayer
from src.Views.single_player import SinglePlayer

class Mode:
    def __init__(self, screen, font, main_background, menu, game_mode, click_sound):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.game_mode = game_mode
        self.click_sound = click_sound

    def draw(self):
        easy_mode = Button((290, 150), 230, 50, 'Easy', '#063B14', '#05310E', '#FFFFFF', self.font,
                           self.click_sound)
        midle_mode = Button((290, 250), 230, 50, 'Midle', '#52570A', '#444703', '#FFFFFF', self.font,
                            self.click_sound)
        hard_mode = Button((290, 350), 230, 50, 'Hard', '#3D0606', '#350505', '#FFFFFF', self.font,
                           self.click_sound)
        back = Button((290, 450), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                easy_mode.click(event, lambda:(
                    self.select_mode('Easy')
                ))
                midle_mode.click(event, lambda: (
                    self.select_mode('Middle')
                ))
                hard_mode.click(event, lambda: (
                    self.select_mode('Hard')
                ))

                back.click(event, lambda: (
                    self.menu.draw()
                ))

            easy_mode.draw(self.screen)
            midle_mode.draw(self.screen)
            hard_mode.draw(self.screen)
            back.draw(self.screen)

    def select_mode(self, mode):
        puzzle_size = None
        if mode == 'Easy':
            puzzle_size = (3, 3)
        elif mode == 'Middle':
            puzzle_size = (4, 4)
        else:
            puzzle_size = (5, 5)

        if(self.game_mode == 'Single'):
            SinglePlayer(self.screen, self.font, self.main_background, self.menu, puzzle_size, (self.game_mode, mode), self.click_sound).draw()
        elif(self.game_mode == 'Multiplayer'):
            Multiplayer(self.screen, self.font,  self.main_background, self.menu, puzzle_size, (self.game_mode, mode), self.click_sound).draw()
