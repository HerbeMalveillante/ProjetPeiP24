from rich import print
import pygame
import random
import time


pygame.init()
screen_width = 1200
screen_height = 800
pygame.display.set_caption("Labyrinth")
font = pygame.font.Font("freesansbold.ttf", 20)


class Color(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    darker = (62, 50, 50)
    dark = (80, 60, 60)
    medium = (126, 99, 99)
    light = (168, 124, 124)
    red = (250, 112, 112)
    green = (166, 207, 152)


class Labyrinth(object):
    def __init__(self, width=4, height=4, padding=30):
        self.width = width
        self.height = height
        self.padding = padding
        self.matrix = [[j + i * width for j in range(height)] for i in range(width)]
        self.walls = []
        self.caseSize = self.getCaseSize()

        # Only used for the generation algorithm and the maze solving algorithm.
        # A maze can have a start and an end, but it is not necessary.
        self.start = None
        self.end = None
        # start and end are currently set by the generate function : the start is the first case visited
        # and the end is a random case among the cases that force the algorithm to backtrack
        # We will change this later as the results are suboptimal.

    def draw(self, screen):
        screen.fill(Color.darker)
        for i in range(self.width):
            for j in range(self.height):
                # On dessine la case
                # Si la case est la case de départ, on la remplit en vert
                # Si la case est la case d'arrivée, on la remplit en rouge
                color = Color.dark
                pygame.draw.rect(
                    screen,
                    color,
                    (
                        self.padding // 2 + i * self.caseSize,
                        self.padding // 2 + j * self.caseSize,
                        self.caseSize,
                        self.caseSize,
                    ),
                    1,
                )

                # Si la case est la case de départ ou la case d'arrivée, on dessine un cercle au centre de la case
                if self.matrix[i][j] == self.start or self.matrix[i][j] == self.end:
                    pygame.draw.circle(
                        screen,
                        Color.green if self.matrix[i][j] == self.start else Color.red,
                        (
                            self.padding // 2 + i * self.caseSize + self.caseSize // 2,
                            self.padding // 2 + j * self.caseSize + self.caseSize // 2,
                        ),
                        self.caseSize // 2,
                        3,
                    )

                # on écrit le numéro de la case si la case est assez grande (au moins 35 pixels)
                if self.caseSize > 35:
                    text = font.render(str(self.matrix[i][j]), True, Color.medium)
                    textRect = text.get_rect()
                    textRect.center = (
                        self.padding // 2 + i * self.caseSize + self.caseSize // 2,
                        self.padding // 2 + j * self.caseSize + self.caseSize // 2,
                    )
                    screen.blit(text, textRect)

        # On dessine les murs du labyrinthe
        # Pour dessiner les murs du labyrinthe, on va utiliser la liste des connexions.
        # Chaque case est identifiée par un numéro unique dans la matrice. Une entrée dans la liste des connexions est
        # un tuple de deux nombres, qui sont les numéros des cases connectées par un mur.
        # Le problème, c'est que les murs sont dessinés entre les cases, et non pas sur les cases. Mais il est facile de contourner
        # Ce problème avec un peu de maths.

        for wall in self.walls:
            i = wall[0]
            j = wall[1]

            # Il faut qu'on sache si le mur est horizontal ou vertical.
            # Pour cela, on va comparer l'identifiant des deux cases.
            # Si les deux identifiants sont consécutifs, alors le mur est horizontal.
            # Si les deux identifiants sont séparés par un nombre égal à la largeur du labyrinthe, alors le mur est vertical.
            # Si ce n'est pas le cas, la connexion est invalide.
            if abs(i - j) == 1:
                # Le mur est horizontal
                orientation = "horizontal"
            elif abs(i - j) == self.width:
                # Le mur est vertical
                orientation = "vertical"
            else:
                # La connexion est invalide
                print(f"Invalid connection between {i} and {j}")
                continue

            # On récupère les coordonées du point de départ du mur
            # Pour cela, on va utiliser la fonction getCoordFromCaseId
            # On récupère les coordonées des deux cases
            coord1 = self.getCoordFromCaseId(i)
            coord2 = self.getCoordFromCaseId(j)
            # On récupère le point du milieu entre les deux cases
            milieu = (
                (coord1[0] + coord2[0]) // 2,
                (coord1[1] + coord2[1]) // 2,
            )
            # On récupère les coordonées du point de départ du mur.
            # Si le mur est horizontal, on prend le point du milieu,
            # Et on décale le point de départ de la moitié de la taille d'une case vers la gauche.
            # Si le mur est vertical, on prend le point du milieu,
            # Et on décale le point de départ de la moitié de la taille d'une case vers le haut.
            # Le point d'arrivée est calculé de la même manière, mais on décale le point de la moitié de la taille d'une case vers la droite ou vers le bas.
            if orientation == "horizontal":
                startPoint = (
                    milieu[0] - self.caseSize // 2,
                    milieu[1],
                )
                endPoint = (
                    milieu[0] + self.caseSize // 2,
                    milieu[1],
                )
            else:
                startPoint = (
                    milieu[0],
                    milieu[1] - self.caseSize // 2,
                )
                endPoint = (
                    milieu[0],
                    milieu[1] + self.caseSize // 2,
                )
            # On dessine le mur
            pygame.draw.line(screen, Color.light, startPoint, endPoint, 3)

        # On fait une ligne épaisse a l'EXTERIEUR de tout le labyrinthe
        pygame.draw.rect(
            screen,
            Color.light,
            (
                self.padding // 2,
                self.padding // 2,
                self.width * self.caseSize,
                self.height * self.caseSize,
            ),
            3,
        )

    def getCaseSize(self):
        return min(
            (screen_height - self.padding) // self.height,
            (screen_width - self.padding) // self.width,
        )

    def getCoordFromCaseId(self, caseId):
        # returns the coordinates of the center of the case on the screen
        i = caseId // self.height
        j = caseId % self.height
        return (
            self.padding // 2 + i * self.caseSize + self.caseSize // 2,
            self.padding // 2 + j * self.caseSize + self.caseSize // 2,
        )

    def isAdjacent(self, case1, case2):
        # returns True if the two cases are adjacent, False otherwise
        # Two cases are adjacent if they are next to each other horizontally or vertically
        # We can check if two cases are adjacent by comparing their caseId
        # If the difference between the caseIds is 1, then the two cases are adjacent horizontally
        # If the difference between the caseIds is equal to the width of the labyrinth, then the two cases are adjacent vertically
        # Otherwise, the two cases are not adjacent
        return abs(case1 - case2) == 1 or abs(case1 - case2) == self.width

    def getAdjacentCases(self, caseId):
        # returns a list of the caseIds of the cases adjacent to the case with the given caseId
        # We can get the caseId of the case above the current case by subtracting the width of the labyrinth from the caseId
        # We can get the caseId of the case below the current case by adding the width of the labyrinth to the caseId
        # We can get the caseId of the case to the left of the current case by subtracting 1 from the caseId
        # We can get the caseId of the case to the right of the current case by adding 1 to the caseId
        # We need to check if the caseId is valid before adding it to the list
        adjacentCases = []
        if caseId - self.width >= 0:
            adjacentCases.append(caseId - self.width)
        if caseId + self.width < self.width * self.height:
            adjacentCases.append(caseId + self.width)
        if caseId % self.width != 0:
            adjacentCases.append(caseId - 1)
        if (caseId + 1) % self.width != 0:
            adjacentCases.append(caseId + 1)
        return adjacentCases

    def addWall(self, case1, case2):
        if not self.isAdjacent(case1, case2):
            print(f"Invalid connection between {case1} and {case2}")
            return
        if case1 > case2:
            case1, case2 = case2, case1
        if not (case1, case2) in self.walls:
            self.walls.append((case1, case2))
        else:
            print(f"Wall between {case1} and {case2} already exists")

    def removeWall(self, case1, case2):
        if not self.isAdjacent(case1, case2):
            print(f"Invalid connection between {case1} and {case2}")
            return
        if case1 > case2:
            case1, case2 = case2, case1
        if (case1, case2) in self.walls:
            self.walls.remove((case1, case2))
        else:
            print(f"Wall between {case1} and {case2} does not exist")

    def fillWithWalls(self):
        for i in range(self.width * self.height):
            if i >= self.width * self.height - 1:
                continue
            localIterator = i % self.width
            if (i + 1) % self.width > localIterator:
                self.addWall(i, i + 1)

            # vertical
            if i + self.width < self.width * self.height:
                self.addWall(i, i + self.width)

    def generate(self):
        print(f"Generating labyrinth of size {self.width} by {self.height}")
        startTime = time.time()

        # La liste des cases courantes est une pile.
        # On commence avec un labyrinthe plein de murs.
        # On va choisir une case au hasard qui va être notre case de départ.
        # On l'appelle la case courante, et on la place au sommet de la pile.
        # On garde une liste des cases visitées.
        # A Chaque étape, on va choisir au hasard une case adjacente à la case courante qui n'a jamais été visitée.
        # On casse le mur entre la case courante et la case choisie, et on fait de la case choisie la case courante.
        # On place la case courante au sommet de la pile.
        # Si aucune case adjacente n'a jamais été visitée, on doit faire demi tour : on dépile la pile pour revenir à la case précédente.

        # Quand la pile est vide, on a visité toutes les cases du labyrinthe.

        self.fillWithWalls()
        visitedCases = []
        stack = []
        currentCase = random.randint(0, self.width * self.height - 1)
        self.start = currentCase
        potentialEnds = (
            []
        )  # On garde une liste des cases qui nous forcent à faire demi tour

        stack.append(currentCase)
        visitedCases.append(currentCase)

        while len(stack) > 0:
            # On récupère la case courante
            currentCase = stack[-1]
            # On récupère les cases adjacentes à la case courante
            adjacentCases = self.getAdjacentCases(currentCase)
            # On récupère les cases adjacentes qui n'ont jamais été visitées
            unvisitedAdjacentCases = [
                case for case in adjacentCases if not case in visitedCases
            ]
            # Si aucune case adjacente n'a jamais été visitée, on doit faire demi tour
            if len(unvisitedAdjacentCases) == 0:
                # On ajoute la case courante à la liste des cases qui nous forcent à faire demi tour
                potentialEnds.append(currentCase)
                stack.pop()
                continue
            # On choisit une case adjacente au hasard
            chosenCase = random.choice(unvisitedAdjacentCases)
            # On casse le mur entre la case courante et la case choisie
            self.removeWall(currentCase, chosenCase)
            # On fait de la case choisie la case courante
            currentCase = chosenCase
            # On ajoute la case courante à la liste des cases visitées
            visitedCases.append(currentCase)
            # On place la case courante au sommet de la pile
            stack.append(currentCase)

        # On choisit une case au hasard dans la liste des cases qui nous forcent à faire demi tour : ce sera la case de fin
        self.end = random.choice(potentialEnds)

        print(f"generation complete in {round(time.time() - startTime, 3)} seconds")


L = Labyrinth(50, 50, 30)
screen = pygame.display.set_mode((screen_width, screen_height))
L.generate()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simulation

    # Drawing

    L.draw(screen)

    pygame.display.flip()  # Update the display

# Quit the game
pygame.quit()
