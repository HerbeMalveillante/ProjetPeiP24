from rich import print

import pygame
import time
from graphics import *
from labyrinth import *
from constants import *

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


class Button(Element):
    def __init__(
        self,
        text="Button",
        action=None,
        pos=(0, 0),
        size=(100, 50),
        background=GRAY,
        textColor=WHITE,
    ):
        super().__init__(pos, size, background)
        self.text = text
        self.textColor = textColor
        self.action = action


class LabyrinthWrapper(Element):
    def __init__(self, labyrinth, pos, size):
        super().__init__(pos, size, BLACK)
        self.labyrinth = labyrinth


class LabyrinthFullScreen(SubMenu):

    def __init__(self, parent, labyrinth):
        super().__init__(parent, "Labyrinthe")

        self.labyrinth = LabyrinthWrapper(
            labyrinth, (0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.elements.append(self.labyrinth)

        # Back button on the top right
        self.elements.append(
            Button(
                "Retour",
                action=self.parent.goBack,
                pos=(SCREEN_WIDTH - 110, 10),
                size=(100, 50),
            )
        )


class MainMenu(SubMenu):
    def __init__(self, parent):
        super().__init__(parent, "Menu Principal", color=WHITE)
        self.elements.append(
            Button(text="Play", action=self.parent.play, pos=(10, 10), size=(100, 50))
        )


class Menu(object):

    def __init__(self):

        # On stocke les dernières frames dans une file pour calculer le FPS
        self.frames = []
        self.frameCount = 0
        self.FPS = (
            -1
        )  # Une valeur négative signifie que le FPS n'a pas pu être calculé.

        self.running = True

        # On utilise une pile pour stocker les différents menus affichés. Ainsi, on peut facilement revenir en arrière.

        self.screenStack = [MainMenu(self)]

    def play(self):
        L = Labyrinth(30, 30)
        generationTime = L.generate()
        print(f"Generated in {generationTime} seconds")
        self.screenStack.append(LabyrinthFullScreen(self, L))

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
        G = Graphics()
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

            # DESSIN
            G.drawSubMenu(self.screenStack[-1])  # On dessine l'écran actuel
            G.flip()  # Affiche l'écran (évite les clignotements en dessinant plusieurs objets à la suite)

            # On met à jour le FPS : le titre de la fenêtre est mis à jour, et l'attribut self.FPS est mis à jour.
            self.updateFPS(start)
            self.updateWindowTitle()

        pygame.quit()
