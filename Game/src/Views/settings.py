import pygame
import sys

from src.Models.button import Button


class Settings:
    def __init__(self, screen, font, main_background, menu,  click_sound):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.click_sound = click_sound

    def draw(self):
        if self.click_sound is not None:
            text = "Sound off"
        else:
            text = "Sound on"
        Sound = Button((290, 100), 230, 50, text, '#38083B', '#2D032D', '#FFFFFF', self.font,
                          self.click_sound)


        back = Button((290, 530), 230, 50, 'Exit', '#3D0606', '#350505', '#FFFFFF', self.font, self.click_sound)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                Sound.click(event, lambda: self.menu.draw(False) if text == "Sound off" else self.menu.draw(True))

                back.click(event, lambda: (
                    self.menu.draw()
                ))

            Sound.draw(self.screen)
            back.draw(self.screen)
