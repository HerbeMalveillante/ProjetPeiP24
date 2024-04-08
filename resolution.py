from menufactory import MenuFactory, Button, Text
from labyrinth import Labyrinth
from constants import *
import pygame


class Resolution(MenuFactory):
    """
    The `Resolution` class represents the resolution menu for a labyrinth game.

    Args:
        stack (Stack): The stack used for managing the menu navigation.
        size (int, optional): The size of the labyrinth. Defaults to 24.
        generation_method (str, optional): The generation method for the labyrinth. Defaults to "dead-end-filling".
        resolution_method (str, optional): The resolution method for the labyrinth. Defaults to "recursive-backtracking".
        looping_factor (float, optional): The looping factor for the labyrinth generation. Defaults to 0.1.

    Attributes:
        stack (Stack): The stack used for managing the menu navigation.
        screen (Surface): The pygame surface for rendering the menu.
        labyrinth (Labyrinth): The labyrinth object for generating and resolving the maze.
        buttons (Group): The group of buttons in the menu.
        elements (Group): The group of elements in the menu.
        statusLabel (Text): The label for displaying the status of the generation or resolution.
        sizeLabel (Text): The label for displaying the size of the labyrinth.
        loopingFactorLabel (Text): The label for displaying the looping factor of the labyrinth generation.
        generationTimeLabel (Text): The label for displaying the generation time.
        generationStepLabel (Text): The label for displaying the current generation step.
        resolutionMethodLabel (Text): The label for displaying the resolution method.
        resolutionMethodLabel2 (Text): The label for displaying the resolution method (recursive backtracking).
        resolutionTimeLabel (Text): The label for displaying the resolution time.
        totalMoveCountLabel (Text): The label for displaying the total move count.
        pathLengthLabel (Text): The label for displaying the path length.
        visitedCountLabel (Text): The label for displaying the number of visited cells (recursive backtracking).
        bannedCountLabel (Text): The label for displaying the number of banned cells (recursive backtracking).

    Methods:
        update(clock): Updates the menu elements and labels.
        draw(): Draws the labyrinth and pathfinding images on the screen.
    """

    def __init__(
        self,
        stack,
        size=24,
        generation_method="depth-first-search",
        resolution_method="recursive-backtracking",
        looping_factor=0.1,
    ):
        super().__init__()

        self.stack = stack
        self.screen = pygame.display.get_surface()

        self.labyrinth = Labyrinth(
            (size, size), generation_method, resolution_method, looping_factor
        )  # Create a labyrinth object

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

        # Statistics about the generation and resolution
        self.statusLabel = Text(self.screen.get_width() // 2 + 120, 10, (255, 255, 255), "Statut : Génération")
        self.elements.add(self.statusLabel)
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
        if resolution_method != "a-star":  # On a new line
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
        """
        Updates the menu elements and labels.

        Args:
            clock (Clock): The pygame clock object for managing the frame rate.
        """
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
        """
        Draws the labyrinth and pathfinding images on the screen.

        This works in the same way as in the `Game` class.
        """
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

        # Draw the two layers to the screen.
        self.screen.blit(labyrinth_image, (20, 20))
        self.screen.blit(pathfinding_image, (20, 20))
