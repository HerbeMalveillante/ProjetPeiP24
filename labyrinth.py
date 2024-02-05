from rich import print
import math
import time
import random

# Ce fichier labyrinth contient toutes les fonctions LOGIQUES
# Du labyrinthe (génération, résolution, etc ?)
# Cette classe ne dépend d'aucune fonction graphique et peut parfatement fonctionner
# sans pygame ou avec n'importe quel autre GUI


class Labyrinth:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[j + i * width for j in range(width)] for i in range(height)]
        self.walls = []

        # Par défaut, les cases de départ et de fin se trouvent
        # tout en haut à gauche et tout en bas à droite
        self.start = 0
        self.end = width * height - 1

    def isAdjacent(self, case1, case2):
        # Retourne True si les deux cases se touchent.
        # Retourne False sinon.
        # case1 et case2 sont les identifiants uniques de chaque case.
        return abs(case1 - case2) == 1 or abs(case1 - case2) == self.width

    def getAdjacentCases(self, case):
        # Retourne une liste des identifiants de toutes les cases adjacentes
        # à celle donnée en input.
        adjacent = []
        if case % self.width != 0:
            adjacent.append(case - 1)
        if (case + 1) % self.width != 0:
            adjacent.append(case + 1)
        if case >= self.width:
            adjacent.append(case - self.width)
        if case < self.width * (self.height - 1):
            adjacent.append(case + self.width)
        return adjacent

    def addWall(self, case1, case2):
        # Ajoute un mur entre les cases case1 et case2
        # à la liste des murs. Le programme vérifie
        # Que les cases sont adjacentes avant d'ajouter le mur.
        # Si les cases ne sont pas adjacentes, le mur n'est
        # pas ajouté. Si le mur existe déjà, il n'est pas ajouté.
        # Retourne True si le mur a été ajouté, False sinon.
        # Les cases sont triées par ordre croissant avant d'être ajoutées.
        # Ainsi, le mur (case1, case2) est le même que le mur (case2, case1).
        if not self.isAdjacent(case1, case2):
            return False
        if case1 > case2:
            case1, case2 = case2, case1
        if (case1, case2) in self.walls:
            return False
        self.walls.append((case1, case2))
        return True

    def removeWall(self, case1, case2):
        # Fonctionne de façon similaire à addWall, mais retire le mur.
        # Retourne True si le mur a été retiré, False sinon.

        if not self.isAdjacent(case1, case2):
            return False
        if case1 > case2:
            case1, case2 = case2, case1
        if (case1, case2) not in self.walls:
            return False
        self.walls.remove((case1, case2))
        return True

    def fillWithWalls(self):
        # Ajoute tous les murs possibles au labyrinthe.
        # Il est important de noter que le contour extérieur
        # Du labyrinthe n'est pas généré.
        # Cette fonction est optimisée de façon à placer intelligemment
        # les murs plutôt que d'utiliser le failsafe de la fonction
        # addWall.

        for i in range(self.width * self.height):
            if i >= self.width * self.height - 1:
                continue
            localIterator = i % self.width
            # Horizontal
            if (i + 1) % self.width > localIterator:
                self.addWall(i, i + 1)
            # Vertical
            if i + self.width < self.width * self.height:
                self.addWall(i, i + self.width)

    def generate(self, loopingFactor=0.05):
        # Génère le labyrinthe en utilisant un algorithme
        # de type "recursive backtracking".
        # L'algorithme est implémenté en utilisant une pile
        # Plutôt qu'une récursion, pour des raisons de performance.
        # L'argument "loopingFactor" est un nombre entre 0 et 1
        # représentant la probabilité qu'un mur soit retiré après la
        # génération afin de créer des boucles dans un labyrinthe
        # qui serait autrement mathématiquement parfait.

        # On chronomètre le temps de génération qui sera retourné
        start = time.time()

        # On commence par ajouter tous les murs possibles
        self.fillWithWalls()

        # On initialise la pile et la liste des cases visitées
        visitedCases = []
        stack = []
        currentCase = random.randint(0, self.width * self.height - 1)
        stack.append(currentCase)
        visitedCases.append(currentCase)

        while len(stack) > 0:  # Tant que la pile n'est pas vide

            currentCase = stack[-1]
            adjacentCases = self.getAdjacentCases(currentCase)
            unvisitedAdjacentCases = [
                case for case in adjacentCases if case not in visitedCases
            ]
            # On récupère les cases adjacentes non visitées.
            # Si aucune case ne correspond, on "backtrack".
            # Sinon, on casse un mur, on fait de la nouvelle case la casse courante et on continue.
            if len(unvisitedAdjacentCases) == 0:
                stack.pop()
                continue
            else:
                nextCase = random.choice(unvisitedAdjacentCases)
                self.removeWall(currentCase, nextCase)
                visitedCases.append(nextCase)
                stack.append(nextCase)

        # On retire des murs pour créer des boucles.
        # La probabilité qu'un mur soit retiré est détemrinée par la variable loopingFactor.
        # Cette variable représente la probabilité qu'un mur soit retiré.
        for wall in self.walls:
            if random.random() < loopingFactor:
                self.removeWall(wall[0], wall[1])

        return round(time.time() - start, 3)
