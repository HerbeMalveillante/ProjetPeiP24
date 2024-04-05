import pygame
from constants import WIDTH, BUTTON_COLOR
from menuresolutioncustom import Resolution_Custom
from game import Game
from menufactory import MenuFactory, Button, Text


class Menu:
    def __init__(self):

        self.quit = False

        self.screen = pygame.display.get_surface()

        self.stack = []
        self.stack.append(Main_Menu(self.stack))

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
    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.elements.add(Text(WIDTH / 2 - 90, 10, (255, 255, 255), "Labyrinthe"))

        self.buttons.add(
            Button(
                WIDTH / 2 - 90,
                53,
                180,
                30,
                BUTTON_COLOR,
                "Résolution Custom",
                self.resolution_custom,
            )
        )

        self.buttons.add(Button(WIDTH / 2 - 90, 93, 180, 30, BUTTON_COLOR, "Jouer", self.start_game))

        self.buttons.add(
            Button(
                WIDTH / 2 - 90,
                133,
                180,
                30,
                BUTTON_COLOR,
                "Quitter",
                exit,
            )
        )

    def resolution_custom(self):
        self.stack.append(Resolution_Custom(self.stack))

    def start_game(self):
        self.stack.append(Game(self.stack))
