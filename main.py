import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Boilerplate")

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic

    # Drawing on the screen
    screen.fill((255, 255, 255))  # Fill the screen with white color

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
