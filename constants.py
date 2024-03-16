import pygame

pygame.font.init()

WIDTH, HEIGHT = 1200, 700


BG_COLOR = (40, 42, 53)
BUTTON_COLOR = (24, 23, 33)
LABYRINTH_RESOLUTION = 60  # in pixels

CHARACTER_COLOR = (139, 233, 253)
POINTS_COLOR = (255, 209, 67)
POINTS_COLOR_2 = (181, 143, 30)
ENEMIES_COLOR = (222, 75, 53)
WHITE = (255, 255, 255)

DRAW_CASE_NUMBERS = False


font_file = "customFont.ttf"
font = pygame.font.Font(font_file, 16)
font_big = pygame.font.Font(font_file, 32)
