import pygame


class Button:
    def __init__(self, pos, width, height, text, color, bottom_color, text_color, font):
        # Core attributes
        self.elevation = 6
        self.dynamic_elevation = 6
        self.original_y_pos = pos[1]
        self.pressed = False

        # Top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = color

        # Bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color

        # Text
        self.text = font.render(text, True, text_color)
        self.text_rect = self.text.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)

        screen.blit(self.text, self.text_rect)

    def click(self, event, func=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.top_rect.collidepoint(event.pos):
                self.pressed = True
                self.dynamic_elevation = 0
                pygame.mixer.music.load('../assets/Sounds/Buttonclick.wav')
                pygame.mixer.music.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                self.dynamic_elevation = self.elevation
                if func is not None:
                    func()
