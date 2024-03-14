import pygame

from src.Models.button import Button
from src.Models.puzzle import Puzzle


class SinglePlayer:
    def __init__(self, screen, font, main_background, menu, puzzle_size):
        self.screen = screen
        self.font = font
        self.main_background = main_background
        self.menu = menu
        self.puzzle_size = puzzle_size

    def draw(self):
        back = Button((290, 550), 230, 50, 'Back', '#333333', '#222222', '#FFFFFF', self.font)
        puzzle = Puzzle(self.screen, self.puzzle_size, self.main_background)
        puzzle.puzzle = puzzle.create_puzzle()

        while not puzzle.end:
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

                            if puzzle.end:
                                puzzle.win()
                back.click(event, lambda: (
                    self.menu.draw()
                ))

            back.draw(self.screen)

