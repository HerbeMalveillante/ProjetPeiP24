import pygame
from constants import *
import time


class Graphics(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font18 = pygame.font.Font(None, 18)
        self.font36 = pygame.font.Font(None, 36)
        self.font54 = pygame.font.Font(None, 54)
        pygame.display.set_caption(WINDOW_TITLE)
        # On stocke les 120 dernières frames dans une file pour calculer le FPS
        self.frames = [0] * 120
        self.frameCount = 0

    def getCellSize(self, labyrinth):
        return min(SCREEN_WIDTH // labyrinth.width, SCREEN_HEIGHT // labyrinth.height)

    def getFPS(self):
        return round(1 / (sum(self.frames) / 120), 1)

    def draw(self, labyrinth, caseNumbers=DRAW_CASE_NUMBERS):
        start = time.time()
        self.screen.fill(BLACK)
        self.drawStartEnd(labyrinth)
        self.drawWalls(labyrinth)
        if caseNumbers:
            self.drawCaseNumbers(labyrinth)
        pygame.display.flip()

        # On calcule le FPS
        self.frames.pop(0)
        self.frames.append(time.time() - start)
        self.frameCount += 1
        if SHOW_FPS and self.frameCount % 60 == 0:
            # Change the title of the window to display the FPS
            pygame.display.set_caption(f"{WINDOW_TITLE} | {self.getFPS()} fps")

    def drawWalls(self, labyrinth):
        # The walls are described as a list of tuples (case1, case2).
        # The list of tuple do not contain the outer edges of the labyrinth.
        # The cases are identified by their unique id, which is their position
        # in the matrix.
        CELL_SIZE = self.getCellSize(labyrinth)

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
                            ((j + 1) * CELL_SIZE, i * CELL_SIZE),
                            ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE),
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
                            (j * CELL_SIZE, (i + 1) * CELL_SIZE),
                            ((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE),
                            2,
                        )
        # Draw the outer edges of the labyrinth
        pygame.draw.rect(
            self.screen,
            WHITE,
            (0, 0, CELL_SIZE * labyrinth.width, CELL_SIZE * labyrinth.height),
            2,
        )

    def drawCaseNumbers(self, labyrinth):
        # Draw the number of each case in the middle of the case
        # We want to adapt the font used to the size of the case.
        # We have three available fonts : 18, 36 and 54.
        # We choose the biggest font that fits in the case.
        # If the case is too small, we do not draw the number.
        # It is important to keep in mind that numbers are drawn in the middle and can
        # contain up to 3 characters.

        CELL_SIZE = self.getCellSize(labyrinth)

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
                        j * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2,
                        i * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2,
                    ),
                )

    def drawStartEnd(self, labyrinth):
        # Draw the start and end cases in a different color (green and red)
        CELL_SIZE = self.getCellSize(labyrinth)
        x1 = labyrinth.start % labyrinth.width
        y1 = labyrinth.start // labyrinth.width
        x2 = labyrinth.end % labyrinth.width
        y2 = labyrinth.end // labyrinth.width
        pygame.draw.rect(
            self.screen, GREEN, (x1 * CELL_SIZE, y1 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
        pygame.draw.rect(
            self.screen, RED, (x2 * CELL_SIZE, y2 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
