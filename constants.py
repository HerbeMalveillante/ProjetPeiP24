import pygame

pygame.font.init()  # Initialize the font module to use custom fonts.

WIDTH, HEIGHT = 1200, 700  # The width and height of the game window.


BG_COLOR = (40, 42, 53)  # The background color of the game window.
BUTTON_COLOR = (24, 23, 33)  # The color of the buttons in the game window.
LABYRINTH_RESOLUTION = 120  # The size of the cells in the labyrinth, in pixel. The image for the labyrinth is created separately in a virtual buffer, then resized and drawn on the screen.
LINE_WIDTH = (
    LABYRINTH_RESOLUTION // 10
)  # The width of the walls in the labyrinth. This is dynamically calculated based on the labyrinth resolution.

CHARACTER_COLOR = (139, 233, 253)  # The color of the character sprite.
POINTS_COLOR = (255, 209, 67)  # The color of the points in the labyrinth.
POINTS_COLOR_2 = (181, 143, 30)  # The color of the points in the labyrinth.
ENEMIES_COLOR = (222, 75, 53)  # The color of the enemies in the labyrinth.
WHITE = (255, 255, 255)

DRAW_CASE_NUMBERS = False  # Flag indicating if the cell numbers should be drawn on the labyrinth. Useful for debugging, but makes the game less visually appealing.
# This debug option also does not take into account the resolution of the labyrinth, so the numbers may be barely visible or overlap with the walls at higher resolutions

# The font used for the game. This font is loaded from a custom TTF file.
font_file = "customFont.ttf"
font = pygame.font.Font(font_file, 16)  # Used for buttons
font_big = pygame.font.Font(font_file, 32)  # Used for text
