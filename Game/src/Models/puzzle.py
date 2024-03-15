import os
import random
import pygame
import re


class Puzzle:
    def __init__(self, screen, puzzle_size, main_background, click_sound):
            self.screen = screen
            self.puzzle_size = puzzle_size
            self.main_background = main_background
            self.pos = (180, 80)
            self.image_path = None
            self.image = self.load_and_scale_image('../assets/Images')
            self.puzzle_size = puzzle_size
            self.winner = False
            self.puzzle = None
            self.selected_piece = None
            self.end = False
            self.click_sound = click_sound

    def load_and_scale_image(self, folder_path):
        files = os.listdir(folder_path)
        random_image = random.choice(files)
        random_image_path = os.path.join(folder_path, random_image)
        self.image_path = random_image_path

        loaded_image = pygame.image.load(random_image_path)
        scaled_image = pygame.transform.scale(loaded_image, (450, 450))
        return scaled_image

    def create_puzzle(self):
        puzzle = []
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]
        pieces_order = [(i, j) for i in range(self.puzzle_size[0]) for j in range(self.puzzle_size[1])]
        random.shuffle(pieces_order)
        for i, j in pieces_order:
            piece_x = i * cell_width
            piece_y = j * cell_height
            piece_width = cell_width
            piece_height = cell_height
            puzzle.append(self.image.subsurface(piece_x, piece_y, piece_width, piece_height))
        return puzzle, pieces_order

    def render_image_parts(self):
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]

        # Draw each piece of the puzzle
        for i in range(self.puzzle_size[0]):
            for j in range(self.puzzle_size[1]):
                screen_x = self.pos[0] + i * cell_width
                screen_y = self.pos[1] + j * cell_height
                self.screen.blit(self.puzzle[i + j * self.puzzle_size[0]],
                                 (self.pos[0] + i * cell_width, self.pos[1] + j * cell_height))

                # Draw a frame around the selected piece
                if self.selected_piece == (i, j):
                    pygame.draw.rect(self.screen, '#008000', (screen_x, screen_y, cell_width, cell_height), 5)

        # Draw lines between the puzzle pieces
        for i in range(self.puzzle_size[0] + 1):
            line_x = self.pos[0] + i * cell_width
            pygame.draw.line(self.screen, (255, 255, 255), (line_x, self.pos[1]),
                             (line_x, self.pos[1] + self.image.get_height()))

        for j in range(self.puzzle_size[1] + 1):
            line_y = self.pos[1] + j * cell_height
            pygame.draw.line(self.screen, (255, 255, 255), (self.pos[0], line_y),
                             (self.pos[0] + self.image.get_width(), line_y))

    def get_clicked_piece(self, mouse_pos):
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]

        for i in range(self.puzzle_size[0]):
            for j in range(self.puzzle_size[1]):
                piece_rect = pygame.Rect(self.pos[0] + i * cell_width, self.pos[1] + j * cell_height, cell_width,
                                         cell_height)
                if piece_rect.collidepoint(mouse_pos):
                    if self.click_sound is not None:
                        pygame.mixer.music.load('../assets/Sounds/PartSelection.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play()
                    return i, j
        return None

    def swap_pieces(self, piece1, piece2, gamer=None):
        index1 = piece1[0] + piece1[1] * self.puzzle_size[0]
        index2 = piece2[0] + piece2[1] * self.puzzle_size[0]
        self.puzzle[index1], self.puzzle[index2] = self.puzzle[index2], self.puzzle[index1]

        if self.is_puzzle_solved():
            self.render_image_parts()
            if gamer is not None:
                if gamer:
                    self.winner = True
                    self.win()
                else:
                    self.winner = False
                    self.lost()
            self.end = True

    def is_puzzle_solved(self):
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]

        for j in range(self.puzzle_size[1]):
            for i in range(self.puzzle_size[0]):
                original_piece = self.image.subsurface(i * cell_width, j * cell_height, cell_width, cell_height)
                current_piece = self.puzzle[i + j * self.puzzle_size[0]]
                for y in range(cell_height):
                    for x in range(cell_width):
                        if original_piece.get_at((x, y)) != current_piece.get_at((x, y)):
                            return False

        return True

    def win(self):
        self.screen.blit(self.main_background, (0, 0))
        self.render_image_parts()
        font = pygame.font.SysFont(None, 60)
        text = font.render('Win!', True, (0, 255, 0))
        text_shadow = font.render('Win!', True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))

        # Отображение "Win!" над фоном, без стирания фона
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text, text_rect)

        pygame.display.update()

        if self.click_sound is not None:
            pygame.mixer.music.load('../assets/Sounds/Win.mp3')
            pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        self.end = True

    def lost(self):
        self.screen.blit(self.main_background, (0, 0))
        self.render_image_parts()
        font = pygame.font.SysFont(None, 60)
        text = font.render("You've lost", True, (0, 255, 0))
        text_shadow = font.render("You've lost", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, 50))
        shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))

        # Отображение "Win!" над фоном, без стирания фона
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text, text_rect)

        pygame.display.update()

        if self.click_sound is not None:
            pygame.mixer.music.load('../assets/Sounds/gameover.mp3')
            pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def create_puzzle_fixed(self, image, puzzle_size, pieces_order):
        puzzle = []
        cell_width = image.get_width() // puzzle_size[0]
        cell_height = image.get_height() // puzzle_size[1]
        for i, j in pieces_order:
            piece_x = i * cell_width
            piece_y = j * cell_height
            piece_width = cell_width
            piece_height = cell_height
            puzzle.append(image.subsurface(piece_x, piece_y, piece_width, piece_height))
        return puzzle

    def pieces_order_to_string(self, pieces_order, image_url):
        order_string = ','.join([f'({x},{y})' for x, y in pieces_order])
        return f"{order_string}|{image_url}"

    def string_to_pieces_order(self, string):
        match = re.match(r'\((\d+),(\d+)\)', string)
        if match:
            pieces_order = []
            for match in re.findall(r'\((\d+),(\d+)\)', string):
                x, y = map(int, match)
                pieces_order.append((x, y))
            image_url = string.split('|')[-1]
            return pieces_order, image_url
