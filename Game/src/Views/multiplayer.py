import socket
import pygame

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

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.socket.connect((ip_address, 10000))

        self.socket.setblocking(False)

        self.move = None
        self.draw()

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)
        puzzle = Puzzle(self.screen, self.puzzle_size, self.main_background)
        check = False

        while True:
            pygame.display.update()
            self.screen.blit(self.main_background, (0, 0))

            # This block of code creates and sends image or accepts, it
            # must be executed only once, therefore there is a variable 'check'

            if not check:
                response = self.socket.recv(1080249).decode()

                if response == "Send":
                    puzzle.puzzle = puzzle.create_puzzle()
                    data = puzzle.to_string(puzzle.puzzle)
                    self.socket.send(data.encode())
                    self.move = True
                else:
                    puzzle.puzzle = puzzle.from_string(response)

                check = True

            for event in pygame.event.get():
                if self.move:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_piece = puzzle.get_clicked_piece(mouse_pos)
                        if clicked_piece:
                            if not puzzle.selected_piece:
                                puzzle.selected_piece = clicked_piece
                            else:
                                puzzle.swap_pieces(puzzle.selected_piece, clicked_piece)
                                data = f"{puzzle.selected_piece}|{clicked_piece}"
                                self.socket.send(data.encode())
                                puzzle.selected_piece = None
                                self.move = False
                else:
                    try:
                        response = self.socket.recv(1024).decode()

                        parts = response.split("|")
                        tuples = [tuple(map(int, part.strip("()").split(", "))) for part in parts]

                        puzzle.swap_pieces(tuples[0], tuples[1])
                        self.move = True
                    except:
                        pass
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            puzzle.render_image_parts()

            back.draw(self.screen)
