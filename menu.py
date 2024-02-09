from rich import print

import pygame
import time
from graphics import *
from labyrinth import *
from constants import *
from character import *

# La classe Menu représente l'interface du jeu.
# Elle est responsable de l'affichage des menus, de la gestion des événements, etc.
# Elle dépend de la classe Graphics pour afficher les menus.

# La classe Menu est responsable de la boucle principale du jeu, de la gestion des événements, de l'affichage des menus, etc.
# Les classes Screen et Button sont des classes internes à Menu, et sont utilisées pour représenter les différents écrans et boutons du jeu.


class Element(object):
    def __init__(self, pos, size, background):
        self.pos = pos
        self.size = size
        self.background = background

        # Get the name of the class that inherits from Element and store it into a TYPE attribute.
        # The graphics function will know how to draw the element based on its type.
        self.TYPE = self.__class__.__name__


class SubMenu(object):
    def __init__(self, parent, name, color=BLACK):
        self.parent = parent
        self.name = name
        self.elements = []
        self.color = color

    def registerInput(self, key):
        pass


class Button(Element):
    def __init__(
        self,
        text="Button",
        action=None,
        pos=(0, 0),
        size=None,
        background=GRAY,
        textColor=WHITE,
    ):
        if size is None:
            size = (
                len(text) * 20,
                50,
            )  # On calcule la taille du bouton en fonction de la longueur du texte (experimental)
        super().__init__(pos, size, background)
        self.text = text
        self.textColor = textColor
        self.action = action


class Text(Element):
    # On veut pouvoir ajouter une ligne de texte à l'écran.
    # On peut incorporer des variables à afficher dans le texte.

    def __init__(
        self,
        text="Hello World !",
        pos=(0, 0),
        size=None,
        textColor=WHITE,
        variables=None,
    ):

        # Les variables sont des fonctions qui renvoient une valeur à afficher.

        self.text = text
        self.pos = pos
        self.textColor = textColor
        self.variables = variables
        if size is None:
            size = (len(text) * 20, 50)
        super().__init__(pos, size, BLACK)


class LabyrinthWrapper(Element):
    def __init__(self, labyrinth, pos=(0, 0), size=(SCREEN_WIDTH, SCREEN_HEIGHT)):
        super().__init__(pos, size, BLACK)
        self.labyrinth = labyrinth
        self.character = Character(labyrinth)  # Devra peut-être être déplacé plus tard


class LabyrinthFullScreen(SubMenu):

    def __init__(self, parent, labyrinth):
        super().__init__(parent, "Labyrinthe")

        self.labyrinth = LabyrinthWrapper(labyrinth)
        self.elements.append(self.labyrinth)

        # Back button on the top right
        self.elements.append(
            Button(
                "Retour",
                action=self.parent.goBack,
                pos=(SCREEN_WIDTH - 200, 10),
            )
        )
        # ScreenShot button on the bottom right
        self.elements.append(
            Button(
                "ScreenShot",
                action=self.parent.G.screenShot,
                pos=(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 60),
            )
        )

    def registerInput(self, key):
        if key == pygame.K_UP:
            self.labyrinth.character.move((0, -1))
        elif key == pygame.K_DOWN:
            self.labyrinth.character.move((0, 1))
        elif key == pygame.K_LEFT:
            self.labyrinth.character.move((-1, 0))
        elif key == pygame.K_RIGHT:
            self.labyrinth.character.move((1, 0))


class LabyrinthResolution(SubMenu):
    def __init__(self, parent, labyrinth):
        super().__init__(parent, "Résolution")

        self.labyrinth = LabyrinthWrapper(labyrinth)
        self.labyrinth.character = None  # On retire le personnage pour la résolution

        self.elements.append(self.labyrinth)

        # Back button on the top right
        self.elements.append(
            Button(
                "Retour",
                action=self.parent.goBack,
                pos=(SCREEN_WIDTH - 200, 10),
            )
        )

        self.elements.append(
            Button("Retry", action=self.parent.retry, pos=(SCREEN_WIDTH - 200, 70))
        )

        self.elements.append(
            Text(
                text="Case actuelle : {v}",
                pos=(SCREEN_WIDTH - 220, 130),
                # On utilise la fonction "labyrinth.getCurrentCase()" pour afficher la case actuelle de façon dynamique
                # Pour ce faire on utilise une fonction lambda
                variables=[self.labyrinth.labyrinth.getCurrentCase],
                textColor=WHITE,
            )
        )
        self.elements.append(
            Text(
                text="Nombre de cases visitées : {v}",
                pos=(SCREEN_WIDTH - 220, 150),
                variables=[self.labyrinth.labyrinth.getVisitedCasesCount],
                textColor=WHITE,
            )
        )
        self.elements.append(
            Text(
                text="Nombre de cases bannies : {v}",
                pos=(SCREEN_WIDTH - 220, 170),
                variables=[self.labyrinth.labyrinth.getBannedCasesCount],
                textColor=WHITE,
            )
        )
        self.elements.append(
            Text(
                text="Nombre total de mouvements : {v}",
                pos=(SCREEN_WIDTH - 220, 190),
                variables=[self.labyrinth.labyrinth.getMovesCount],
                textColor=WHITE,
            )
        )

        # On veut ajouter du texte avec des stats sur la résolution


class MainMenu(SubMenu):
    def __init__(self, parent):
        super().__init__(parent, "Menu Principal", color=WHITE)
        self.elements.append(
            Button(text="Play", action=self.parent.play, pos=(10, 10), size=(100, 50))
        )
        self.elements.append(
            Button(
                "Résolution automatique",
                action=self.parent.resolve,
                pos=(10, 70),
                size=(200, 50),
            )
        )

        # Quit button
        self.elements.append(
            Button(
                "Quitter",
                action=lambda: setattr(
                    self.parent, "running", False
                ),  # Modify attribute with a lambda function
                pos=(10, 130),
                size=(100, 50),
            )
        )


class Menu(object):

    def __init__(self):

        # On stocke les dernières frames dans une file pour calculer le FPS
        self.frames = []
        self.frameCount = 0
        self.FPS = (
            -1
        )  # Une valeur négative signifie que le FPS n'a pas pu être calculé.
        self.G = Graphics()

        self.running = True

        # On utilise une pile pour stocker les différents menus affichés. Ainsi, on peut facilement revenir en arrière.

        self.screenStack = [MainMenu(self)]

    def play(self):
        L1 = Labyrinth(20, 20)
        generationTime = L1.generate()

        print(f"Generated in {generationTime} seconds")
        self.screenStack.append(LabyrinthFullScreen(self, L1))

    def resolve(self):
        L = Labyrinth(100, 100)
        generationTime = L.generate()
        solvingTime = L.resolve_animate()
        print(f"Generated in {generationTime} seconds")
        print(f"Solved in {solvingTime} seconds")
        self.screenStack.append(LabyrinthResolution(self, L))

    def retry(self):
        self.screenStack.pop()
        self.resolve()

    def goBack(self):
        self.screenStack.pop()

    def updateFPS(self, start):

        dt = round(time.time() - start, 5)
        self.frames.append(dt)

        if sum(self.frames) > FPS_RESOLUTION:

            calculated = round(len(self.frames) / sum(self.frames))
            self.FPS = calculated
            # On retire les vieilles frames
            while sum(self.frames) > FPS_RESOLUTION:
                self.frames.pop(0)

    def updateWindowTitle(self):
        info = [WINDOW_TITLE]
        # On affiche le FPS dans le titre de la fenêtre.
        if SHOW_FPS:
            info.append(f"{self.FPS} FPS")

        info.append(self.screenStack[-1].name)

        # On récupère le nom de la fenêtre pour vérifier si le titre a changé.
        currentTitle = pygame.display.get_caption()[0]
        if currentTitle != " - ".join(info):
            pygame.display.set_caption(" - ".join(info))

    def main(self):
        while self.running:

            start = time.time()  # On prend une mesure du temps au début de la frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in self.screenStack[-1].elements:
                        if button.TYPE == "Button":
                            if (
                                button.pos[0]
                                < event.pos[0]
                                < button.pos[0] + button.size[0]
                                and button.pos[1]
                                < event.pos[1]
                                < button.pos[1] + button.size[1]
                            ):
                                if button.action:
                                    button.action()
                elif event.type == pygame.KEYUP:
                    self.screenStack[-1].registerInput(event.key)

            # DESSIN
            self.G.drawSubMenu(self.screenStack[-1])  # On dessine l'écran actuel
            self.G.flip()  # Affiche l'écran (évite les clignotements en dessinant plusieurs objets à la suite)

            # On met à jour le FPS : le titre de la fenêtre est mis à jour, et l'attribut self.FPS est mis à jour.
            self.updateFPS(start)
            self.updateWindowTitle()

        pygame.quit()
