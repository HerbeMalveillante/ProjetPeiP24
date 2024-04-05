import menufactory
import pygame
from resolution import Resolution
from constants import BUTTON_COLOR


class Resolution_Custom(menufactory.MenuFactory):

    def __init__(self, stack):
        super().__init__()

        self.stack = stack
        self.screen = pygame.display.get_surface()

        text1 = menufactory.Text(10, 10, (255, 255, 255), "Custom Resolution")
        self.elements.add(text1)

        buttonResolution = menufactory.Button(
            10, 50, 200, 30, BUTTON_COLOR, "Générer et Résoudre", self.initiate_solve
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

    def initiate_solve(self):
        # Retrieve the correct data from the inputs and create the corresponding resolution
        # add the resolution to the stack
        self.stack.append(Resolution(self.stack))

    def draw(self):
        super().draw()
