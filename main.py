import pygame
import constants
from menu import Menu


def main():
    """
    The main function of the game.
    Initializes the game, sets up the display, and runs the game loop.
    """
    pygame.init()  # Initialize the game engine.
    clock = pygame.time.Clock()  # Create a clock object to track time.
    pygame.display.set_caption("Labyrinthe")  # Set the title of the game window.
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))  # Create the game window.

    menu = Menu()  # Create the main menu object.

    running = True
    while running:
        running = menu.update(clock)  # Update the main menu and check if the game should continue running.

        screen.fill(constants.BG_COLOR)  # Fill the screen with the background color.
        menu.draw()  # Draw the main menu on the screen.
        pygame.display.flip()  # Update the display.

        # Display the resolution and the number of frames per second in the window title.
        resolution = str(screen.get_width()) + "x" + str(screen.get_height())
        pygame.display.set_caption(f"Labyrinthe - {resolution} - {int(clock.get_fps())} FPS")


main()  # Run the main function to start the game.
