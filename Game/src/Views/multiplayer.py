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

            if self.move is not None:
                if self.move:
                    self.move_draw("Your move")
                else:
                    self.move_draw("The opponent's move")

            # This block of code creates and sends image or accepts, it
            # must be executed only once, therefore there is a variable 'check'

            if not check:
                response = self.socket.recv(1080249).decode()

                if response == "Send":
                    puzzle.puzzle = puzzle.create_puzzle()
                    data = puzzle.to_string(puzzle.puzzle, puzzle.image_path)
                    self.socket.send(data.encode())

                    self.move = True
                else:
                    puzzle.puzzle, image_path = puzzle.from_string(response)

                    loaded_image = pygame.image.load(image_path)
                    puzzle.image = pygame.transform.scale(loaded_image, (450, 450))

                    self.move = False

                check = True

            for event in pygame.event.get():
                if self.move:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_piece = puzzle.get_clicked_piece(mouse_pos)
                        if clicked_piece:
                            if not puzzle.selected_piece:
                                puzzle.selected_piece = clicked_piece
                            elif clicked_piece == puzzle.selected_piece:
                                puzzle.selected_piece = None
                            else:
                                puzzle.swap_pieces(puzzle.selected_piece, clicked_piece, True)

                                data = f"{puzzle.selected_piece}|{clicked_piece}"
                                self.socket.send(data.encode())
                                if puzzle.end:
                                    self.menu.draw()

                                puzzle.selected_piece = None
                                self.move = False
                                pygame.display.update()

                else:
                    try:
                        response = self.socket.recv(1024).decode()

                        parts = response.split("|")
                        tuples = [tuple(map(int, part.strip("()").split(", "))) for part in parts]

                        puzzle.swap_pieces(tuples[0], tuples[1], False)
                        if puzzle.end:
                            self.menu.draw()

                        self.move = True
                        pygame.display.update()

                    except:
                        pass
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            puzzle.render_image_parts()

            back.draw(self.screen)

    def move_draw(self, message):
        font = pygame.font.SysFont(None, 40)
        text = font.render(message, True, (0, 255, 0))
        text_shadow = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))

        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text, text_rect)