from rich import print
import math
import time
import random
from uuid import uuid4  # Pour donner un identifiant unique au labyrinthe

# Ce fichier labyrinth contient toutes les fonctions LOGIQUES
# Du labyrinthe (génération, résolution, etc ?)
# Cette classe ne dépend d'aucune fonction graphique et peut parfatement fonctionner
# sans pygame ou avec n'importe quel autre GUI


class Labyrinth:
    def __init__(self, width, height):
        self.id = (
            uuid4()
        )  # On donne un identifiant unique au labyrinthe (utilisé pour le cache)
        self.width = width
        self.height = height
        self.matrix = [[j + i * width for j in range(width)] for i in range(height)]
        self.walls = []
        self.hasChanged = True  # Indique si le labyrinthe a changé depuis la dernière fois qu'il a été dessiné. (= s'il doit être redessiné)
        self.solvingData = None  # Contient les données de résolution du labyrinthe
        self.solved = False
        self.generationTime = None

        # Par défaut, les cases de départ et de fin se trouvent
        # tout en haut à gauche et tout en bas à droite
        self.start = 0
        self.end = width * height - 1

    def isAdjacent(self, case1, case2):
        # Retourne True si les deux cases se touchent.
        # Retourne False sinon.
        # case1 et case2 sont les identifiants uniques de chaque case.
        case1, case2 = min(case1, case2), max(case1, case2)
        return case1 in self.getAdjacentCases(case2)

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
        self.hasChanged = True
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
        self.hasChanged = True
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
        self.hasChanged = True

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

        self.hasChanged = True
        self.generationTime = round(time.time() - start, 3)
        return self.generationTime

    def canMove(self, case1, case2):

        case1, case2 = min(case1, case2), max(case1, case2)

        if not self.isAdjacent(case1, case2):
            return False

        if (case1, case2) in self.walls:
            return False

        return True

    def resolve(self):

        # Retourne une liste des cases à parcourir pour résoudre le labyrinthe.
        # Pour un premier essai, on va implémenter l'algorithme "Dead-end filling".
        # Cet algorithme consiste à reconnaître quand on arrive dans un cul-de-sac et à revenir en arrière jusqu'à la dernière intersection.

        # On commence par la case du début
        # Si on a une intersection, on choisit un chemin au hasard
        # Quand on arrive à un cul de sac, on dépile jusqu'à la dernière intersection en gardant trace des cases dépilées
        # On considère que ces cases n'existent plus à la prochaine étape et on recommence

        # On chronomètre le temps de résolution qui sera retourné
        start = time.time()

        stack = [self.start]  # Notre chemin actuel
        banned = []
        visited = []
        totalMoveCount = 0

        while (
            stack[-1] != self.end
        ):  # Tant qu'on est pas arrivé à la dernière case du labyrinthe
            # On choisit une direction au hasard parmi les cases disponibles non visitées
            available = [
                i
                for i in self.getAdjacentCases(stack[-1])
                if self.canMove(stack[-1], i)
            ]

            available = [
                i for i in available if i not in banned and i not in visited
            ]  # On enlève les cases bannies des cases visitables

            if available == []:  # Cul de sac ! On dépile
                banned.append(stack.pop())
            else:

                # La case est ajoutée à la pile et marquée comme visitée
                stack.append(random.choice(available))
                visited.append(stack[-1])

            totalMoveCount += 1

            self.solvingData = {  # On stocke les données de résolution du labyrinthe
                "moves": stack,
                "banned": banned,
                "visited": visited,
                "totalMoveCount": totalMoveCount,
            }

        print(stack)
        self.solved = True
        return round(time.time() - start, 3)

    def resolve_animate(self):

        totalMoveCount = 0

        stack, banned, visited, totalMoveCount = (
            (
                self.solvingData["moves"],
                self.solvingData["banned"],
                self.solvingData["visited"],
                self.solvingData["totalMoveCount"],
            )
            if self.solvingData is not None
            else ([self.start], [], [], 0)
        )

        if stack[-1] == self.end:
            self.solved = True
            return True

        # Fonctionne de la même manière que resolve, mais n'effectue qu'une seule itération à la fois.
        # On choisit une direction au hasard parmi les cases disponibles non visitées
        available = [
            i for i in self.getAdjacentCases(stack[-1]) if self.canMove(stack[-1], i)
        ]

        available = [
            i for i in available if i not in banned and i not in visited
        ]  # On enlève les cases bannies des cases visitables

        if available == []:  # Cul de sac ! On dépile
            banned.append(stack.pop())
        else:

            # La case est ajoutée à la pile et marquée comme visitée
            stack.append(random.choice(available))
            visited.append(stack[-1])

        # On incrémente le nombre de moves
        totalMoveCount += 1

        self.solvingData = {  # On stocke les données de résolution du labyrinthe
            "moves": stack,
            "banned": banned,
            "visited": visited,
            "totalMoveCount": totalMoveCount,
        }

    def getCurrentCase(self):
        return self.solvingData["moves"][-1]

    def getBannedCasesCount(self):
        return len(self.solvingData["banned"])

    def getVisitedCasesCount(self):
        return len(self.solvingData["visited"])

    def getMovesCount(self):
        return self.solvingData["totalMoveCount"]
