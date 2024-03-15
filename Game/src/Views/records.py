import pygame

from src.Models.button import Button


class Records:
    def __init__(self, screen, font, main_background, menu):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu

        self.draw()

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)

        while True:
            pygame.display.update()
            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # data =


    def move_draw(self, message):
        font = pygame.font.SysFont(None, 40)
        text = font.render(message, True, (0, 255, 0))
        text_shadow = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))

        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text, text_rect)