import pygame
import json

from src.Models.button import Button
from src.Models.puzzle import Puzzle


class SinglePlayer:
    def __init__(self, screen, font, main_background, menu, puzzle_size, data, click_sound):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.puzzle_size = puzzle_size
        self.data = data
        self.start_time = 0
        self.duration = 0
        self.click_sound = click_sound

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)
        puzzle = Puzzle(self.screen, self.puzzle_size, self.main_background, self.click_sound)
        puzzle.puzzle, none = puzzle.create_puzzle()

        if self.data[1] == 'Easy':
            self.start_timer(60000)
        elif self.data[1] == 'Middle':
            self.start_timer(120000)
        else:
            self.start_timer(180000)


        while not puzzle.end:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            if self.draw_timer():
                puzzle.lost()
                self.menu.draw()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_piece = puzzle.get_clicked_piece(mouse_pos)
                    if clicked_piece:
                        if not puzzle.selected_piece:
                            puzzle.selected_piece = clicked_piece
                        else:
                            puzzle.swap_pieces(puzzle.selected_piece, clicked_piece, True)
                            puzzle.selected_piece = None

                            if puzzle.end:
                                self.start_time = (pygame.time.get_ticks() - self.start_time) / 1000
                                if puzzle.winner:
                                    puzzle.winner = "Win"
                                else:
                                    puzzle.winner = "Lose"
                                data = f"{self.data[0]}|{self.data[1]}|{self.start_time}s|{puzzle.winner}||"
                                self.save_data(data)
                                puzzle.win()

                back.click(event, lambda: (
                    self.menu.draw()
                ))

            puzzle.render_image_parts()
            back.draw(self.screen)

    def start_timer(self, duration):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        remaining_time = max(self.duration - elapsed_time, 0)
        return remaining_time

    def draw_timer(self):
        remaining_time = self.update_timer()
        timer_text = self.font.render(f"Time left: {int(remaining_time / 1000)}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))
        if int(remaining_time) / 1000 == 0:
            return True

    def save_data(self, new_data):
            with open("Statistics.json", 'r') as file:
                data = json.load(file)

            data += new_data

            with open("Statistics.json", 'w') as file:
                json.dump(data, file)
