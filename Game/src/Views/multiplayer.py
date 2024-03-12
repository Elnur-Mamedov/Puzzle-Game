import socket
import pygame
import json

from src.Models.button import Button
from src.Models.puzzle import Puzzle


class Multiplayer:
    def __init__(self, screen, font, main_background, menu, puzzle_size=(4, 4)):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.puzzle_size = puzzle_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        with open('ipadress.json', 'r') as f:
            ip_adress = f.read().strip('"\n')
            print(ip_adress)
        self.socket.connect((ip_adress, 10000))
        self.draw()

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)
        puzzle = Puzzle(self.screen, self.puzzle_size, self.main_background)

        json_data = None

        with open('p.json', 'r') as f:
            json_data = f.read()

        puzzle.puzzle = Puzzle.from_json(json_data)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            puzzle.render_image_parts()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_piece = puzzle.get_clicked_piece(mouse_pos)
                    if clicked_piece:
                        if not puzzle.selected_piece:
                            puzzle.selected_piece = clicked_piece
                        else:
                            puzzle.swap_pieces(puzzle.selected_piece, clicked_piece)
                            puzzle.selected_piece = None
                            puzzle_data = Puzzle.to_json(puzzle.puzzle)

                            with open('p.json', 'w') as f:
                                json.dump(puzzle_data, f)
                                print('Puzzle saved')
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            back.draw(self.screen)
