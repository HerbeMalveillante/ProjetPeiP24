import pygame
from constants import WIDTH, HEIGHT, BUTTON_COLOR
from labyrinth import Labyrinth
from game import Game
from menufactory import MenuFactory, Button, Text


class Menu:
    def __init__(self):

        self.quit = False

        self.screen = pygame.display.get_surface()

        self.stack = [Main_Menu(self)]

    def update(self, clock):

        if self.quit:
            return False

        self.stack[-1].update(clock)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.stack[-1].on_click(event.pos)

            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.stack[-1].on_key(event.key, event.type == pygame.KEYDOWN)
        return True

    def draw(self):
        self.stack[-1].draw()

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            self.quit = True


class Main_Menu(MenuFactory):
    def __init__(self, parent):
        super().__init__(parent)

        self.elements.add(Text(self, WIDTH / 2 - 90, 10, (255, 255, 255), "Labyrinthe"))

        self.buttons.add(
            Button(
                self,
                WIDTH / 2 - 90,
                53,
                180,
                30,
                BUTTON_COLOR,
                "Résolution Custom",
                self.resolution_custom,
            )
        )

        self.buttons.add(Button(self, WIDTH / 2 - 90, 93, 180, 30, BUTTON_COLOR, "Jouer", self.start_game))

        self.buttons.add(
            Button(
                self,
                WIDTH / 2 - 90,
                133,
                180,
                30,
                BUTTON_COLOR,
                "Quitter",
                self.parent.back,
            )
        )

    def resolution_custom(self):
        self.parent.stack.append(Resolution(self))

    def start_game(self):
        self.parent.stack.append(Game(self))


class Resolution(MenuFactory):
    """
    Cette classe permet d'afficher la génération, puis la résolution du labyrinthe.
    On aura un autre menu entre le menu principal et celui-ci, qui permettra de choisir les options de génération et de résolution qui seront passés en paramètres.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.labyrinth = Labyrinth(self, (20, 20), "dead-end-filling", "recursive-backtracking", 0.1)

    def update(self, clock):
        clock.tick()
        if not self.labyrinth.generation_data["is_generated"]:
            self.labyrinth.generate_step()
        else:
            if not self.labyrinth.resolution_data["is_solved"]:
                self.labyrinth.resolve_step()

    def draw(self):
        labyrinth_image = self.labyrinth.get_image()
        labyrinth_image_height = labyrinth_image.get_size()[1]
        displayable_height = HEIGHT - 40
        ratio = displayable_height / labyrinth_image_height
        labyrinth_image = pygame.transform.scale(
            labyrinth_image, (int(ratio * labyrinth_image.get_size()[0]), displayable_height)
        )
        pathfinding_image = self.labyrinth.get_pathfinding_image()
        pathfinding_image = pygame.transform.scale(
            pathfinding_image, (int(ratio * pathfinding_image.get_size()[0]), displayable_height)
        )

        # On la dessine à l'écran
        self.parent.parent.screen.blit(labyrinth_image, (20, 20))
        self.parent.parent.screen.blit(pathfinding_image, (20, 20))
