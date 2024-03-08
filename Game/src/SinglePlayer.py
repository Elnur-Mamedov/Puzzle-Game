import pygame
import random

from src.button import Button

class SinglePlayer:
    def __init__(self, screen, font, main_background, menu, image_file_name, image_size, pos, puzzle_size=(4, 4)):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.image = self.load_and_scale_image(image_file_name, image_size)
        self.pos = pos
        self.puzzle_size = puzzle_size
        self.scramble_moves = 0
        self.puzzle = self.create_puzzle()
        self.selected_piece = None

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)

        while True:
            pygame.display.update()

            self.screen.blit(self.main_background, (0, 0))

            self.render_image_parts()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_piece = self.get_clicked_piece(mouse_pos)
                    if clicked_piece:
                        if not self.selected_piece:
                            self.selected_piece = clicked_piece
                        else:
                            self.swap_pieces(self.selected_piece, clicked_piece)
                            self.selected_piece = None
                back.click(event, lambda: (
                    self.menu.draw()
                ))


            back.draw(self.screen)
        pygame.quit()

    def get_clicked_piece(self, mouse_pos):
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]

        for i in range(self.puzzle_size[0]):
            for j in range(self.puzzle_size[1]):
                piece_rect = pygame.Rect(self.pos[0] + i * cell_width, self.pos[1] + j * cell_height, cell_width,
                                         cell_height)
                if piece_rect.collidepoint(mouse_pos):
                    return (i, j)
        return None

    def swap_pieces(self, piece1, piece2):
        index1 = piece1[0] + piece1[1] * self.puzzle_size[0]
        index2 = piece2[0] + piece2[1] * self.puzzle_size[0]
        self.puzzle[index1], self.puzzle[index2] = self.puzzle[index2], self.puzzle[index1]

        if self.is_puzzle_solved():
            self.win()

    def load_and_scale_image(self, image_file_name, image_size):
        loaded_image = pygame.image.load(image_file_name)
        scaled_image = pygame.transform.scale(loaded_image, image_size)
        return scaled_image

    def create_puzzle(self):
        puzzle = []
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]
        pieces = [(i, j) for i in range(self.puzzle_size[0]) for j in range(self.puzzle_size[1])]
        random.shuffle(pieces)
        for i, j in pieces:
            puzzle.append(self.image.subsurface(i * cell_width, j * cell_height, cell_width, cell_height))
        return puzzle

    def render_image_parts(self):
        cell_width = self.image.get_width() // self.puzzle_size[0]
        cell_height = self.image.get_height() // self.puzzle_size[1]

        # Draw each piece of the puzzle
        for i in range(self.puzzle_size[0]):
            for j in range(self.puzzle_size[1]):
                screen_x = self.pos[0] + i * cell_width
                screen_y = self.pos[1] + j * cell_height
                self.screen.blit(self.puzzle[i + j * self.puzzle_size[0]], (self.pos[0] + i * cell_width, self.pos[1] + j * cell_height))

        # Draw lines between the puzzle pieces
        for i in range(self.puzzle_size[0] + 1):
            line_x = self.pos[0] + i * cell_width
            pygame.draw.line(self.screen, (255, 255, 255), (line_x, self.pos[1]),
                             (line_x, self.pos[1] + self.image.get_height()))

        for j in range(self.puzzle_size[1] + 1):
            line_y = self.pos[1] + j * cell_height
            pygame.draw.line(self.screen, (255, 255, 255), (self.pos[0], line_y),
                             (self.pos[0] + self.image.get_width(), line_y))

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
        self.menu.draw()