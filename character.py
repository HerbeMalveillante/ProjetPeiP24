import constants
from rich import print


import labyrinth


class Character(object):
    def __init__(self, labyrinth):
        self.labyrinth = labyrinth
        self.pos = self.labyrinth.start
        self.moveCount = 0

    def move(self, direction):
        # direction can either be (1, 0), (-1, 0), (0, 1) or (0, -1).
        allowedDirections = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # direction cannot be (0, 0), (1, 1), (-1, -1), (1, -1) or (-1, 1).
        if direction not in allowedDirections:
            return False

        # Mouvement horizontal
        if direction[0] != 0:
            newPos = self.pos + direction[0]
        # Mouvement vertical
        elif direction[1] != 0:
            newPos = self.pos + direction[1] * self.labyrinth.width

        if not self.labyrinth.canMove(self.pos, newPos):
            return

        self.pos = newPos
