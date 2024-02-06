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
        # direction cannot be (0, 0), (1, 1), (-1, -1), (1, -1) or (-1, 1).

        # We check if the move is possible
        if direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if direction == (1, 0):
                targetWall = min(self.pos, self.pos + 1), max(self.pos, self.pos + 1)
                if self.pos % self.labyrinth.width != self.labyrinth.width - 1:
                    if targetWall not in self.labyrinth.walls:
                        self.pos += 1
                        self.moveCount += 1
            elif direction == (-1, 0):
                targetWall = min(self.pos, self.pos + 1), max(self.pos, self.pos + 1)
                if self.pos % self.labyrinth.width != 0:
                    if targetWall not in self.labyrinth.walls:
                        self.pos -= 1
                        self.moveCount += 1
            elif direction == (0, 1):
                targetWall = min(self.pos, self.pos + self.labyrinth.width), max(
                    self.pos, self.pos + self.labyrinth.width
                )
                if self.pos < self.labyrinth.width * (self.labyrinth.height - 1):
                    if targetWall not in self.labyrinth.walls:
                        self.pos += self.labyrinth.width
                        self.moveCount += 1
            elif direction == (0, -1):
                targetWall = min(self.pos, self.pos + self.labyrinth.width), max(
                    self.pos, self.pos + self.labyrinth.width
                )
                if self.pos >= self.labyrinth.width:
                    if targetWall not in self.labyrinth.walls:
                        self.pos -= self.labyrinth.width
                        self.moveCount += 1
        else:
            print("Invalid direction")
            return False
