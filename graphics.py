import pygame
from constants import *
import time
import os

# Ce fichier contient les classes et fonctions graphiques
# Il dépend de pygame et ne peut pas fonctionner sans.
# La plupart des fonctions de cette classe permettent de dessiner des objets spécifiques,
# comme par exemple un labyrinthe.
# La logique du programme peut fonctionner sans problème sans cette classe.


# Note sur le cache : pour éviter de recalculer le labyrinthe à chaque frame, on stocke
# La surface sur laquelle le labyrinthe est dessiné dans un dictionnaire.
# Chaque labyrinthe a un identifiant unique et un attribut qui indique si le labyrinthe a changé depuis
# La dernière fois qu'il a été dessiné. Si le labyrinthe a changé, on le redessine, sinon on affiche simplement la surface.


class Graphics(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font18 = pygame.font.Font(None, 18)
        self.font36 = pygame.font.Font(None, 36)
        self.font54 = pygame.font.Font(None, 54)
        self.cache = {}
        pygame.display.set_caption(WINDOW_TITLE)

    def clearScreen(self, color=BLACK):
        self.screen.fill(color)

    def flip(self):
        pygame.display.flip()

    def screenShot(self):
        # Save a screenshot of the current screen
        # Si il n'y a pas de dossier screenshots, il est créé.
        # Le screenshot est enregistré sous le nom screenshot{annee-mois-jour--heure-minutes-secondes}.png
        # Si un screenshot a déjà été pris à cette seconde, on ajoute un nombre à la fin du nom.
        # On retourne le nom du screenshot.

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        name = "screenshots/screenshot" + time.strftime("%Y-%m-%d--%H-%M-%S") + ".png"
        i = 0
        while os.path.exists(name):
            i += 1
            name = (
                "screenshots/screenshot"
                + time.strftime("%Y-%m-%d--%H-%M-%S")
                + f"({i}).png"
            )
        pygame.image.save(self.screen, name)
        print(f"Screenshot saved as {name}")
        return name

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

    def labyrinthSurface(
        self,
        labyrinth,
        size=(SCREEN_WIDTH, SCREEN_HEIGHT),
        caseNumbers=DRAW_CASE_NUMBERS,
    ):
        # On dessine le labyrinthe sur une nouvelle surface et on retourne cette surface

        # On fait une nouvelle surface
        # On veut que la taille de la surface soit de la taille donnée en entrée.

        surface = pygame.Surface(size)

        self.drawStartEnd(labyrinth, size, surface)
        self.drawWalls(labyrinth, size, surface)
        self.drawOuterEdges(labyrinth, size, surface)
        if caseNumbers:
            self.drawCaseNumbers(labyrinth, size, surface)

        # on retourne la surface
        return surface

    def drawWalls(self, labyrinth, size, surface):
        CELL_SIZE = self.getCellSize(labyrinth, size)
        WALL_COLOR = WHITE
        WALL_THICKNESS = 2

        # On veut dessiner les murs du labyrinthe.
        # Chaque mur est représenté par deux cases, qui doivent être séparées par un mur.
        # Un mur peut être vertical ou horizontal.

        # Commençons donc par regarder si le mur est horizontal ou vertical.
        # Le mur est horizontal si les deux cases sont sur la même ligne.

        for w in labyrinth.walls:
            if (
                abs(w[0] - w[1]) == 1
            ):  # les deux cases sont sur la même ligne : le mur est vertical
                orientation = "V"
            elif (
                abs(w[0] - w[1]) == labyrinth.width
            ):  # les deux cases sont sur la même colonne : le mur est horizontal
                orientation = "H"
            else:
                print("ERREUR : les deux cases ne sont pas adjacentes")

            # On dessine le mur en fonction de son orientation.
            # Le mur est une ligne qui sépare les deux cases.
            # On récupère les coordonées du coin supérieur gauche des deux cases
            topLeft1 = (
                w[0] % labyrinth.width * CELL_SIZE,
                w[0] // labyrinth.width * CELL_SIZE,
            )
            topLeft2 = (
                w[1] % labyrinth.width * CELL_SIZE,
                w[1] // labyrinth.width * CELL_SIZE,
            )
            if orientation == "H":
                # Le point de départ de la ligne se situe sur topLeft2
                # La ligne fait la taille d'une case donc le point d'arrivée est (topLeft2[0] + CELL_SIZE, topLeft2[1])
                pygame.draw.line(
                    surface,
                    WALL_COLOR,
                    (topLeft2[0], topLeft2[1]),
                    (topLeft2[0] + CELL_SIZE, topLeft2[1]),
                    WALL_THICKNESS,
                )
            else:
                pygame.draw.line(
                    surface,
                    WALL_COLOR,
                    (topLeft2[0], topLeft2[1]),
                    (topLeft2[0], topLeft2[1] + CELL_SIZE),
                    WALL_THICKNESS,
                )

    def drawOuterEdges(self, labyrinth, size, surface):
        CELL_SIZE = self.getCellSize(labyrinth, size)
        WALL_COLOR = WHITE
        WALL_THICKNESS = 2
        pygame.draw.rect(
            surface,
            WALL_COLOR,
            (0, 0, CELL_SIZE * labyrinth.width, CELL_SIZE * labyrinth.height),
            WALL_THICKNESS,
        )

    def drawStartEnd(self, labyrinth, size, surface):
        CELL_SIZE = self.getCellSize(labyrinth, size)
        x1 = labyrinth.start % labyrinth.width
        y1 = labyrinth.start // labyrinth.width
        x2 = labyrinth.end % labyrinth.width
        y2 = labyrinth.end // labyrinth.width
        pygame.draw.rect(
            surface,
            GREEN,
            (x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
        pygame.draw.rect(
            surface,
            RED,
            (x2 * CELL_SIZE, y2 * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )

    def drawCaseNumbers(self, labyrinth, size, surface):
        CELL_SIZE = self.getCellSize(labyrinth, size)

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

                text = font.render(text, ANTIALIASING, (255, 255, 255))
                surface.blit(
                    text,
                    (
                        j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2,
                        i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2,
                    ),
                )

    def drawButton(self, button):
        # Draw the button on the screen
        pygame.draw.rect(self.screen, button.background, (button.pos, button.size))
        # Calculate the font to use based on the size of the button and the length of the text to display
        if len(button.text) > 10:
            font = self.font18
        elif len(button.text) > 5:
            font = self.font36
        else:
            font = self.font54
        text = font.render(button.text, ANTIALIASING, button.textColor)
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
                # Le labyrinthe possède un attribut "hasChanged" qui indique si il a été modifié.
                # Cet attribut prend la valeur "True" dès qu'une modification est apportée au labyrinthe.
                # Si l'attribut est "False", on peut simplement dessiner la surface stockée dans le cache."
                # Si l'attribut est "True", on redessine le labyrinthe et on stocke la nouvelle surface dans le cache.
                # Comme la dernière version du labyrinthe est stockée dans le cache, on peut passer l'attribut "hasChanged" à "False".
                if (
                    element.labyrinth.id not in self.cache
                    or element.labyrinth.hasChanged
                ):
                    self.cache[element.labyrinth.id] = self.labyrinthSurface(
                        element.labyrinth, element.size
                    )

                    element.labyrinth.hasChanged = False
                # On dessine le labyrinthe
                self.screen.blit(self.cache[element.labyrinth.id], element.pos)

                # On dessine le personnage
                self.drawCharacter(element.character)

    def drawCharacter(self, character):
        CELL_SIZE = self.getCellSize(character.labyrinth, (SCREEN_WIDTH, SCREEN_HEIGHT))
        x = character.pos % character.labyrinth.width
        y = character.pos // character.labyrinth.width
        pygame.draw.rect(
            self.screen,
            BLUE,
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )
