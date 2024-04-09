import menufactory
import pygame
from resolution import Resolution
from constants import BUTTON_COLOR


class Resolution_Custom(menufactory.MenuFactory):
    """
    A custom resolution menu class that allows the user to customize the maze generation and solving parameters.

    Attributes:
        stack (list): A list representing the stack of menus.
        screen (pygame.Surface): The surface of the pygame display.
        grid_size (int): The size of the maze grid.
        looping_factor (float): The looping factor for maze generation.
    """

    def __init__(self, stack):
        """
        Initializes a Resolution_Custom object.

        Args:
            stack (list): A list representing the stack of menus.
        """
        super().__init__()

        self.stack = stack
        self.screen = pygame.display.get_surface()

        self.grid_size = 24  # The default grid size is 24.
        self.looping_factor = 0.10  # The default looping factor is 0.10.

        text1 = menufactory.Text(10, 10, (255, 255, 255), "Génération et Résolution personnalisée")
        self.elements.add(text1)

        buttonResolution = menufactory.Button(
            20, self.screen.get_height() - 50, 200, 30, BUTTON_COLOR, "Générer et Résoudre", self.initiate_solve
        )
        self.buttons.add(buttonResolution)

        button_back = menufactory.Button(
            self.screen.get_width() - 100,
            self.screen.get_height() - 50,
            80,
            30,
            BUTTON_COLOR,
            "Retour",
            self.stack.pop,
        )
        self.buttons.add(button_back)

        # Grid size selection
        grid_size_text = menufactory.Text(10, 100, (255, 255, 255), "Taille de la grille")
        self.elements.add(grid_size_text)

        # Buttons to increase and decrease the grid size
        button_1 = menufactory.Button(10, 150, 30, 30, BUTTON_COLOR, "-", self.decrease_grid_size)
        self.buttons.add(button_1)

        self.grid_size_label = menufactory.Text(
            button_1.image.get_width() + 20, 140, (255, 255, 255), str(self.grid_size)
        )
        self.elements.add(self.grid_size_label)

        button_2 = menufactory.Button(
            self.grid_size_label.image.get_width() + 10 + button_1.image.get_width() + 20,
            150,
            30,
            30,
            BUTTON_COLOR,
            "+",
            self.increase_grid_size,
        )
        self.buttons.add(button_2)

        # Buttons to select the maze generation method
        generation_text = menufactory.Text(10, 200, (255, 255, 255), "Méthode de génération")
        self.elements.add(generation_text)
        self.generation_label = menufactory.Text(10, 240, (255, 255, 255), "depth-first-search")
        self.elements.add(self.generation_label)
        # generation_button = menufactory.Button(10, 280, 100, 40, BUTTON_COLOR, "Changer", self.toggle_generation)
        # self.buttons.add(generation_button)
        # ^^^ This line may be uncommented to add a button to toggle between generation methods if any is implemented later on.

        # Button to select the maze solving method
        resolution_text = menufactory.Text(10, 340, (255, 255, 255), "Méthode de résolution")
        self.elements.add(resolution_text)
        self.resolution_label = menufactory.Text(10, 380, (255, 255, 255), "recursive-backtracking")
        self.elements.add(self.resolution_label)
        resolution_button = menufactory.Button(10, 420, 100, 40, BUTTON_COLOR, "Changer", self.toggle_resolution)
        self.buttons.add(resolution_button)

        # Looping factor selection
        looping_factor_text = menufactory.Text(10, 480, (255, 255, 255), "Looping factor")
        self.elements.add(looping_factor_text)

        button_3 = menufactory.Button(
            10,
            530,
            30,
            30,
            BUTTON_COLOR,
            "-",
            self.decrease_looping_factor,
        )
        self.buttons.add(button_3)
        self.looping_factor_label = menufactory.Text(
            10 + button_3.image.get_width() + 10, 520, (255, 255, 255), str(self.looping_factor)
        )
        self.elements.add(self.looping_factor_label)
        button_4 = menufactory.Button(
            self.looping_factor_label.image.get_width() + 10 + 10 + button_3.image.get_width() + 30,
            530,
            30,
            30,
            BUTTON_COLOR,
            "+",
            self.increase_looping_factor,
        )
        self.buttons.add(button_4)

    def increase_grid_size(self):
        """
        Increases the size of the maze grid by 1.
        """
        self.grid_size += 1
        self.grid_size_label.update_text(str(self.grid_size))
        if self.grid_size >= 75:
            print("ATTENTION : Un labyrinthe de taille supérieure à 75x75 peut causer des problèmes d'affichage !")

    def decrease_grid_size(self):
        """
        Decreases the size of the maze grid by 1.
        """
        if self.grid_size > 2:  # The minimum grid size is 2.
            self.grid_size -= 1
            self.grid_size_label.update_text(str(self.grid_size))

    def toggle_resolution(self):
        """
        Toggles between the "a-star" and "recursive-backtracking" maze solving methods.
        """
        if self.resolution_label.text == "a-star":
            self.resolution_label.update_text("recursive-backtracking")
        else:
            self.resolution_label.update_text("a-star")

    def increase_looping_factor(self):
        """
        Increases the looping factor for maze generation by 0.05.
        """
        self.looping_factor += 0.05
        self.looping_factor = round(self.looping_factor, 2)  # Round to 2 decimal places
        self.looping_factor = min(self.looping_factor, 1.0)  # Limit to 1.0
        self.looping_factor_label.update_text(str(self.looping_factor))

    def decrease_looping_factor(self):
        """
        Decreases the looping factor for maze generation by 0.05.
        """
        self.looping_factor -= 0.05
        self.looping_factor = round(self.looping_factor, 2)  # Round to 2 decimal places
        self.looping_factor = max(self.looping_factor, 0.0)  # Limit to 0.0
        self.looping_factor_label.update_text(str(self.looping_factor))

    def initiate_solve(self):
        """
        Initiates the maze generation and solving process by creating a Resolution object with the selected parameters
        and adding it to the stack.
        """
        self.stack.append(
            Resolution(
                self.stack, self.grid_size, self.generation_label.text, self.resolution_label.text, self.looping_factor
            )
        )

    def draw(self):
        """
        Draws the custom resolution menu on the screen.
        """
        super().draw()
