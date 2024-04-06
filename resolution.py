from menufactory import MenuFactory, Button, Text
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

        # On ajoute des statistiques sur la génération et la résolution
        self.statusLabel = Text(self.screen.get_width() // 2 + 120, 10, (255, 255, 255), "Statut : Génération")
        self.elements.add(self.statusLabel)
        # add the labyrinth size and looping factor. This won't need to be updated
        self.sizeLabel = Text(
            self.screen.get_width() // 2 + 120, 35, (255, 255, 255), f"Taille du labyrinthe : {size}x{size}"
        )
        self.elements.add(self.sizeLabel)
        self.loopingFactorLabel = Text(
            self.screen.get_width() // 2 + 120, 60, (255, 255, 255), f"Facteur de bouclage : {looping_factor}"
        )
        self.elements.add(self.loopingFactorLabel)
        self.generationTimeLabel = Text(
            self.screen.get_width() // 2 + 120, 85, (255, 255, 255), "Temps de génération : 0"
        )
        self.elements.add(self.generationTimeLabel)
        self.generationStepLabel = Text(self.screen.get_width() // 2 + 120, 110, (255, 255, 255), "Étape : 0")
        self.elements.add(self.generationStepLabel)

        # Blank space of 25 pixels

        self.resolutionMethodLabel = Text(
            self.screen.get_width() // 2 + 120,
            150,
            (255, 255, 255),
            f"Méthode de résolution : {'A*' if resolution_method == 'a-star' else ''}",
        )
        self.elements.add(self.resolutionMethodLabel)
        if resolution_method != "a-star":  # Sur une nouvelle ligne
            self.resolutionMethodLabel2 = Text(
                self.screen.get_width() // 2 + 120, 175, (255, 255, 255), f"Recursive backtracking"
            )
            self.elements.add(self.resolutionMethodLabel2)

        self.resolutionTimeLabel = Text(
            self.screen.get_width() // 2 + 120, 200, (255, 255, 255), "Temps de résolution : 0"
        )
        self.elements.add(self.resolutionTimeLabel)

        self.totalMoveCountLabel = Text(self.screen.get_width() // 2 + 120, 225, (255, 255, 255), "Étape : 0")
        self.elements.add(self.totalMoveCountLabel)

        self.pathLengthLabel = Text(self.screen.get_width() // 2 + 120, 250, (255, 255, 255), "Longueur du chemin : 0")
        self.elements.add(self.pathLengthLabel)

        # Adding the visited / banned stats only if the resolution method is recursive backtracking
        if self.labyrinth.resolution_algorithm == "recursive-backtracking":
            self.visitedCountLabel = Text(
                self.screen.get_width() // 2 + 120, 275, (255, 255, 255), "Cases visitées : 0"
            )
            self.elements.add(self.visitedCountLabel)
            self.bannedCountLabel = Text(self.screen.get_width() // 2 + 120, 300, (255, 255, 255), "Cases bannies : 0")
            self.elements.add(self.bannedCountLabel)

    def update(self, clock):
        clock.tick()

        # Update the labels
        self.statusLabel.update_text(
            "Statut : Génération" if not self.labyrinth.generation_data["is_generated"] else "Statut : Résolution"
        )
        self.generationTimeLabel.update_text(
            f"Temps de génération : {self.labyrinth.generation_data['generation_time']:.2f}s"
        )
        self.generationStepLabel.update_text(f"Étape : {self.labyrinth.generation_data['action_count']}")

        self.resolutionTimeLabel.update_text(
            f"Temps de résolution : {self.labyrinth.resolution_data['resolution_time']:.2f}s"
        )

        self.totalMoveCountLabel.update_text(f"Étape : {self.labyrinth.resolution_data['total_move_count']}")

        if self.labyrinth.resolution_algorithm == "a-star":
            self.pathLengthLabel.update_text(f"Longueur du chemin : {len(self.labyrinth.resolution_data['path'])}")
        elif self.labyrinth.resolution_algorithm == "recursive-backtracking":
            self.pathLengthLabel.update_text(
                f"Longueur du chemin : {len(self.labyrinth.resolution_data['stack']) - 1}"
            )

            # Updating the visited / banned stats
            self.visitedCountLabel.update_text(f"Cases visitées : {len(self.labyrinth.resolution_data['visited'])}")
            self.bannedCountLabel.update_text(f"Cases bannies : {len(self.labyrinth.resolution_data['banned'])}")

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
