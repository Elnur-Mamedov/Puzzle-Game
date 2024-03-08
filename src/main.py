import pygame

from src.menu import Menu

pygame.init()

screen = pygame.display.set_mode((800, 600), flags=pygame.NOFRAME)

pygame.display.set_caption("Puzzle Game")
pygame.display.set_icon(pygame.image.load('../assets/gameicon.png'))
main_background = pygame.transform.scale(pygame.image.load('../assets/BackgroundImage.jpg'), (800, 600))

font = pygame.font.Font(None, 36)

menu = Menu(screen, font, main_background)

menu.draw()