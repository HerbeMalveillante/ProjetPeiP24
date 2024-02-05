import pygame
from constants import *
import time

# Ce fichier contient les classes et fonctions graphiques
# Il dépend de pygame et ne peut pas fonctionner sans.
# La plupart des fonctions de cette classe permettent de dessiner des objets spécifiques,
# comme par exemple un labyrinthe.
# La logique du programme peut fonctionner sans problème sans cette classe.


class Graphics(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font18 = pygame.font.Font(None, 18)
        self.font36 = pygame.font.Font(None, 36)
        self.font54 = pygame.font.Font(None, 54)
        pygame.display.set_caption(WINDOW_TITLE)

    def clearScreen(self, color=BLACK):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def getCellSize(self, labyrinth, size, pixelPerfect=PIXEL_PERFECT):
        # On calcule la taille de chaque case en fonction de la taille du labyrinthe
        # et de la taille maximale disponible.
        # Par défaut, on accepte des valeurs non-entières pour la taille des cases afin
        # de garantir une certaine cohérence entre les labyrinthes de tailles différentes.
        # On peut forcer la taille des cases à être un entier en passant pixelPerfect=True.
        # Dans ce cas, les labyrinthes seront légèrement plus petits que la taille maximale.
        if pixelPerfect:
            return min(size[0] // labyrinth.width, size[1] // labyrinth.height)
        return min(size[0] / labyrinth.width, size[1] / labyrinth.height)

    def drawLabyrinth(
        self,
        labyrinth,
        pos=(0, 0),
        size=(SCREEN_WIDTH, SCREEN_HEIGHT),
        caseNumbers=DRAW_CASE_NUMBERS,
    ):
        # Par défaut, le labyrinthe est dessiné en haut à gauche de l'écran, et prend toute la place disponible.
        # On aimerait pouvoir le dessiner à un autre endroit, ou avec une taille différente afin de pouvoir
        # L'intégrer au menu et afficher d'autres informations à côté.
        # On peut donc passer en argument la position du coin supérieur gauche du labyrinthe, ainsi que la taille
        # totale du labyrinthe.
        # On considère que tous les labyrinthes sont des carrés : ainsi la taille totale est définie par la taille
        # du plus petit côté.

        start = time.time()
        self.drawStartEnd(labyrinth, pos, size)
        self.drawWalls(labyrinth, pos, size)
        if caseNumbers:
            self.drawCaseNumbers(labyrinth, pos, size)

    def drawWalls(self, labyrinth, pos, size):
        # The walls are described as a list of tuples (case1, case2).
        # The list of tuple do not contain the outer edges of the labyrinth.
        # The cases are identified by their unique id, which is their position
        # in the matrix.
        CELL_SIZE = self.getCellSize(labyrinth, size)

        # The labyrinth is drawn as a grid of cells.
        # A wall is drawn between two cases if there is a wall between them.
        # If the cases are horizontally adjacent, the wall is drawn vertically.
        # If the cases are vertically adjacent, the wall is drawn horizontally.
        # The walls are drawn in white.
        for i in range(labyrinth.height):
            for j in range(labyrinth.width):
                if j != labyrinth.width - 1:
                    if (
                        labyrinth.matrix[i][j],
                        labyrinth.matrix[i][j + 1],
                    ) in labyrinth.walls:
                        pygame.draw.line(
                            self.screen,
                            WHITE,
                            ((j + 1) * CELL_SIZE + pos[0], i * CELL_SIZE + pos[1]),
                            (
                                (j + 1) * CELL_SIZE + pos[0],
                                (i + 1) * CELL_SIZE + pos[1],
                            ),
                            2,
                        )
                if i != labyrinth.height - 1:
                    if (
                        labyrinth.matrix[i][j],
                        labyrinth.matrix[i + 1][j],
                    ) in labyrinth.walls:
                        pygame.draw.line(
                            self.screen,
                            WHITE,
                            (j * CELL_SIZE + pos[0], (i + 1) * CELL_SIZE + pos[1]),
                            (
                                (j + 1) * CELL_SIZE + pos[0],
                                (i + 1) * CELL_SIZE + pos[1],
                            ),
                            2,
                        )
        # Draw the outer edges of the labyrinth
        pygame.draw.rect(
            self.screen,
            WHITE,
            (pos[0], pos[1], CELL_SIZE * labyrinth.width, CELL_SIZE * labyrinth.height),
            2,
        )

    def drawCaseNumbers(self, labyrinth, pos, size):
        # Draw the number of each case in the middle of the case
        # We want to adapt the font used to the size of the case.
        # We have three available fonts : 18, 36 and 54.
        # We choose the biggest font that fits in the case.
        # If the case is too small, we do not draw the number.
        # It is important to keep in mind that numbers are drawn in the middle and can
        # contain up to 3 characters.

        CELL_SIZE = self.getCellSize(labyrinth, pos, size)

        for i in range(labyrinth.height):
            for j in range(labyrinth.width):
                text = str(labyrinth.matrix[i][j])

                # We choose the biggest font that fits in the case based on the length of the text and the
                # size of the case.
                if len(text) > 3:
                    continue
                if CELL_SIZE < 54:
                    font = self.font18
                elif CELL_SIZE < 108:
                    font = self.font36
                else:
                    font = self.font54

                text = font.render(text, 0, (255, 255, 255))
                self.screen.blit(
                    text,
                    (
                        j * CELL_SIZE + pos[0] + CELL_SIZE // 2 - text.get_width() // 2,
                        i * CELL_SIZE
                        + pos[1]
                        + CELL_SIZE // 2
                        - text.get_height() // 2,
                    ),
                )

    def drawStartEnd(self, labyrinth, pos, size):
        # Draw the start and end cases in a different color (green and red)
        CELL_SIZE = self.getCellSize(labyrinth, size)
        x1 = labyrinth.start % labyrinth.width
        y1 = labyrinth.start // labyrinth.width
        x2 = labyrinth.end % labyrinth.width
        y2 = labyrinth.end // labyrinth.width
        pygame.draw.rect(
            self.screen,
            GREEN,
            (x1 * CELL_SIZE + pos[0], y1 * CELL_SIZE + pos[1], CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.rect(
            self.screen,
            RED,
            (x2 * CELL_SIZE + pos[0], y2 * CELL_SIZE + pos[1], CELL_SIZE, CELL_SIZE),
        )

    def drawButton(self, button):
        # Draw the button on the screen
        pygame.draw.rect(self.screen, button.background, (button.pos, button.size))
        text = self.font18.render(button.text, 0, button.textColor)
        self.screen.blit(
            text,
            (
                button.pos[0] + button.size[0] // 2 - text.get_width() // 2,
                button.pos[1] + button.size[1] // 2 - text.get_height() // 2,
            ),
        )

    def drawSubMenu(self, subMenu):
        # Draw the current screen
        self.clearScreen(color=subMenu.color)
        for element in subMenu.elements:
            if element.TYPE == "Button":
                self.drawButton(element)
            elif element.TYPE == "LabyrinthWrapper":
                self.drawLabyrinth(element.labyrinth, element.pos, element.size)
                print(f"Drawing labyrinth at {element.pos} with size {element.size}")
