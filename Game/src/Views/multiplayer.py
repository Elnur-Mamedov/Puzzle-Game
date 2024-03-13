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

            if check:
                try:
                    move = self.socket.recv(1024).decode()
                    if move == "True" or move == "False":
                        self.move = bool(move)
                except:
                    pass

            for event in pygame.event.get():
                # Вот тут если ход его то он выбирает
                # Но если не его он ожидает ход и получает измененный пузл
                # То есть другой изменил че то и отправил но и это не работает

                if self.move:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_piece = puzzle.get_clicked_piece(mouse_pos)
                        if clicked_piece:
                            if not puzzle.selected_piece:
                                puzzle.selected_piece = clicked_piece
                            else:
                                puzzle.swap_pieces(puzzle.selected_piece, clicked_piece)
                                puzzle.selected_piece = None
                                data = puzzle.to_string(puzzle.puzzle)
                                self.socket.send(data.encode())
                else:
                    try:
                        response = self.socket.recv(1080249).decode()
                        puzzle.puzzle = puzzle.from_string(response)
                        puzzle.render_image_parts()

                    except:
                        pass
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            # This block of code creates and sends image or accepts, it
            # must be executed only once, therefore there is a variable 'check'


            # Вот тут например, кто первый тот создает пузл и отправляет второму
            # И это работает, у обеих одно и тоже
            # Но в других местах он че то не работает

            if not check:
                response = self.socket.recv(1080249).decode()

                if response == "Send":
                    puzzle.puzzle = puzzle.create_puzzle()
                    data = puzzle.to_string(puzzle.puzzle)
                    self.socket.send(data.encode())
                    check = True
                else:
                    puzzle.puzzle = puzzle.from_string(response)
                    check = True

            puzzle.render_image_parts()

            back.draw(self.screen)
