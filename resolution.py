from menufactory import MenuFactory, Button
from labyrinth import Labyrinth
from constants import *
import pygame


class Resolution(MenuFactory):
    """
    Cette classe permet d'afficher la génération, puis la résolution du labyrinthe.
    On aura un autre menu entre le menu principal et celui-ci, qui permettra de choisir les options de génération et de résolution qui seront passés en paramètres.
    """

    def __init__(
        self,
        stack,
        size=24,
        generation_method="dead-end-filling",
        resolution_method="recursive-backtracking",
        looping_factor=0.1,
    ):
        super().__init__()

        self.stack = stack
        self.screen = pygame.display.get_surface()

        # self.labyrinth = Labyrinth((24, 24), "dead-end-filling", "recursive-backtracking", 0.1)
        self.labyrinth = Labyrinth((size, size), generation_method, resolution_method, looping_factor)

        quit_button = Button(
            self.screen.get_width() - 100,
            self.screen.get_height() - 50,
            80,
            30,
            BUTTON_COLOR,
            "Retour",
            self.stack.pop,
        )
        self.buttons.add(quit_button)

    def update(self, clock):
        clock.tick()
        if not self.labyrinth.generation_data["is_generated"]:
            self.labyrinth.generate_step()
        else:
            if not self.labyrinth.resolution_data["is_solved"]:
                self.labyrinth.resolve_step()

    def draw(self):

        super().draw()

        labyrinth_image = self.labyrinth.get_image()
        labyrinth_image_height = labyrinth_image.get_size()[1]
        displayable_height = HEIGHT - 40
        ratio = displayable_height / labyrinth_image_height
        labyrinth_image = pygame.transform.scale(
            labyrinth_image, (int(ratio * labyrinth_image.get_size()[0]), displayable_height)
        )
        pathfinding_image = self.labyrinth.get_pathfinding_image()
        pathfinding_image = pygame.transform.scale(
            pathfinding_image, (int(ratio * pathfinding_image.get_size()[0]), displayable_height)
        )

        # On la dessine à l'écran
        self.screen.blit(labyrinth_image, (20, 20))
        self.screen.blit(pathfinding_image, (20, 20))
