import pygame
import sys
import json

from src.Models.button import Button


class Records:
    def __init__(self, json_path, screen, font,  menu):
        self.json_path = json_path
        self.screen = screen
        self.menu = menu
        self.font = font
        self.main_background = pygame.transform.scale(pygame.image.load('../assets/Statics.jpg'), (800, 600))
        self.WIDTH, self.HEIGHT = screen.get_size()

        with open("Statistics.json", 'r') as file:
            json_string = json.load(file)

        self.statistics = self.parse_json(json_string)

        self.scroll_y = 0
        self.scroll_speed = 20

    def parse_json(self, json_string):
        parts = json_string.replace("Your statistics||", "").split("||")
        statistics = []
        for part in parts:
            data = part.split("|")
            if len(data) == 4:
                mode, difficulty, time, result = data
                stat_entry = {
                    "mode": mode,
                    "difficulty": difficulty,
                    "time": time,
                    "result": result
                }
                statistics.append(stat_entry)
        return statistics

    def draw(self):
        back = Button((10, 10), 60, 60, 'Back', '#333333', '#222222', '#FFFFFF', self.font)

        running = True
        while running:
            self.screen.blit(self.main_background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.scroll_y = min(self.scroll_y + self.scroll_speed, 0)
                    elif event.button == 5:
                        max_scroll = max(len(self.statistics) * 60 - self.HEIGHT, 0)
                        self.scroll_y = max(self.scroll_y - self.scroll_speed, -max_scroll)

                back.click(event, lambda: (
                    self.menu.draw()
                ))

            pos = 50 + self.scroll_y
            for stat in self.statistics:
                self.move_draw(f"{stat['mode']} | {stat['difficulty']} | {stat['time']} | {stat['result']}", pos,
                               "#FFFFFF")
                pos += 30
                self.move_draw(f"----------------------------------------", pos, "#FFFFFF")
                pos += 40

            back.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def move_draw(self, message, pos=50, color=(0, 255, 0,), fill_white=False, shadow=False):
        if fill_white:
            self.screen.fill("#FFFFFF")
        font = pygame.font.SysFont(None, 60)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, pos))

        if shadow:
            text_shadow = font.render(message, True, "#FFFFFF")
            shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))
            self.screen.blit(text_shadow, shadow_rect)

        self.screen.blit(text, text_rect)