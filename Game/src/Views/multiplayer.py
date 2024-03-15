import socket
import pygame
import pyodbc
import json

from src.Models.button import Button
from src.Models.puzzle import Puzzle


def get_ip():
    conn_str = f'DRIVER={{SQL Server}};SERVER=sql.bsite.net\MSSQL2016;DATABASE=user001_Puzzle_Game;UID=user001_Puzzle_Game;PWD=Admin2004'

    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    sql_query = '''
    SELECT Ip_Adress
    FROM IP
    WHERE id = 1
    '''

    cursor.execute(sql_query)
    ip = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return ip

class Multiplayer:
    def __init__(self, screen, font, main_background, menu, puzzle_size, data):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.puzzle_size = puzzle_size
        self.start_time = 0
        self.duration = 0
        self.data = data
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        ip_address = get_ip()

        self.socket.connect((ip_address, 10000))

        self.socket.setblocking(False)

        self.move = None
        self.draw()

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)
        puzzle = Puzzle(self.screen, self.puzzle_size, self.main_background)
        check = [False, False, False, True]

        game_stop = pygame.time.get_ticks()

        while True:
            pygame.display.update()
            self.screen.blit(self.main_background, (0, 0))

            if self.move is not None:
                if self.move:
                    self.move_draw("Your move")
                else:
                    self.move_draw("The opponent's move")
            else:
                self.move_draw("We are waiting for the enemy")

            # This block of code creates and sends image or accepts, it
            # must be executed only once, therefore there is a variable 'check'

            if not check[0]:
                response = self.socket.recv(1024).decode()

                if response == "Send":
                    puzzle.puzzle, pieces_order = puzzle.create_puzzle()
                    data = puzzle.pieces_order_to_string(pieces_order, puzzle.image_path)
                    self.socket.send(data.encode())
                else:
                    pieces_order, image_path = puzzle.string_to_pieces_order(response)

                    loaded_image = pygame.image.load(image_path)
                    puzzle.image = pygame.transform.scale(loaded_image, (450, 450))

                    puzzle.puzzle = puzzle.create_puzzle_fixed(puzzle.image, self.puzzle_size, pieces_order)
                    self.move = False
                    check[1] = True

                check[0] = True

            if not check[1]:
                try:
                    start = self.socket.recv(1024).decode()
                    if start == "Start":
                        self.move = True
                        check[1] = True
                except:
                    pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
                                check[2] = True
                                if puzzle.end:
                                    game_stop = (pygame.time.get_ticks() - game_stop) / 1000
                                    if puzzle.winner:
                                        puzzle.winner = "Win"
                                    else:
                                        puzzle.winner = "Lose"
                                    json_data = f"{self.data[0]}|{self.data[1]}|{game_stop}s|{puzzle.winner}"
                                    self.save_data(json_data)
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
                            game_stop = (pygame.time.get_ticks() - game_stop) / 1000
                            if puzzle.winner:
                                puzzle.winner = "Win"
                            else:
                                puzzle.winner = "Lose"
                            json_data = f"{self.data[0]}|{self.data[1]}|{game_stop}s|{puzzle.winner}"
                            self.save_data(json_data)
                            self.menu.draw()

                        self.move = True
                        if check[2]:
                            self.start_timer(21000)
                            check[2] = False
                    except:
                        pass
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            if self.move:
                if check[3]:
                    self.start_timer(21000)
                    check[3] = False
                if self.draw_timer():
                    data = f"(1, 1)|(1, 1)"
                    self.socket.send(data.encode())
                    self.move = False
                    check[2] = True

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

    def start_timer(self, duration):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def update_timer(self, start_time, duration):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = max(duration - elapsed_time, 0)
        return remaining_time

    def draw_timer(self):
        remaining_time = self.update_timer(self.start_time, self.duration)
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
