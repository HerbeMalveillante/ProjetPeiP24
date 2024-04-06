import menufactory
import pygame
from resolution import Resolution
from constants import BUTTON_COLOR


class Resolution_Custom(menufactory.MenuFactory):

    def __init__(self, stack):
        super().__init__()

        self.stack = stack
        self.screen = pygame.display.get_surface()

        self.grid_size = 24
        self.looping_factor = 0.10

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

        # Choix de la taille de la grille
        grid_size_text = menufactory.Text(10, 100, (255, 255, 255), "Taille de la grille")
        self.elements.add(grid_size_text)

        # Boutons pour augmenter ou diminuer la taille de la grille
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

        # Bouton pour sélectionner la méthode de génération
        generation_text = menufactory.Text(10, 200, (255, 255, 255), "Méthode de génération")
        self.elements.add(generation_text)
        self.generation_label = menufactory.Text(10, 240, (255, 255, 255), "dead-end-filling")
        self.elements.add(self.generation_label)
        # generation_button = menufactory.Button(10, 280, 100, 40, BUTTON_COLOR, "Changer", self.toggle_generation)
        # self.buttons.add(generation_button)

        # Bouton pour sélectionner la méthode de résolution
        resolution_text = menufactory.Text(10, 340, (255, 255, 255), "Méthode de résolution")
        self.elements.add(resolution_text)
        self.resolution_label = menufactory.Text(10, 380, (255, 255, 255), "recursive-backtracking")
        self.elements.add(self.resolution_label)
        resolution_button = menufactory.Button(10, 420, 100, 40, BUTTON_COLOR, "Changer", self.toggle_resolution)
        self.buttons.add(resolution_button)

        # Sélection du looping factor
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
        self.grid_size += 1
        self.grid_size_label.update_text(str(self.grid_size))

    def decrease_grid_size(self):
        self.grid_size -= 1
        self.grid_size_label.update_text(str(self.grid_size))

    def toggle_generation(self):
        if self.generation_label.text == "dead-end-filling":
            self.generation_label.update_text("recursive-backtracking")
        else:
            self.generation_label.update_text("dead-end-filling")

    def toggle_resolution(self):
        if self.resolution_label.text == "a-star":
            self.resolution_label.update_text("recursive-backtracking")
        else:
            self.resolution_label.update_text("a-star")

    def increase_looping_factor(self):
        self.looping_factor += 0.05
        self.looping_factor = round(self.looping_factor, 2)
        self.looping_factor = min(self.looping_factor, 1.0)
        self.looping_factor_label.update_text(str(self.looping_factor))

    def decrease_looping_factor(self):
        self.looping_factor -= 0.05
        self.looping_factor = round(self.looping_factor, 2)
        self.looping_factor = max(self.looping_factor, 0.0)
        self.looping_factor_label.update_text(str(self.looping_factor))

    def initiate_solve(self):
        # Retrieve the correct data from the inputs and create the corresponding resolution
        # add the resolution to the stack
        self.stack.append(
            Resolution(
                self.stack, self.grid_size, self.generation_label.text, self.resolution_label.text, self.looping_factor
            )
        )

    def draw(self):
        super().draw()
