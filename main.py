import pygame
import random
import constants
from menu import Menu


def main():

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Labyrinthe")
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

    menu = Menu()

    running = True
    while running:
        running = menu.update(clock)

        screen.fill(constants.BG_COLOR)
        menu.draw()
        pygame.display.flip()

        # Display the resolution and the number of frames per second in the window title.
        resolution = str(screen.get_width()) + "x" + str(screen.get_height())
        pygame.display.set_caption(f"Labyrinthe - {resolution} - {int(clock.get_fps())} FPS")


main()
