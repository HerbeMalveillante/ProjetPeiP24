import pygame
from constants import WIDTH, BUTTON_COLOR
from menuresolutioncustom import Resolution_Custom
from game import Game
from menufactory import MenuFactory, Button, Text


class Menu:
    """
    The main menu class that handles the game menu.

    The stack attribute is a handy way to keep track of the menu screens.
    Each menu screen is a separate class that inherits from the MenuFactory class.
    By storing them in a stack (FILO), we can easily navigate between them by pushing and popping screens.
    This allows us to keep an history of the screens and even store data between them.
    For example, when generating a custom labyrinth, pressing the "back" button will keep the
    Previous settings instead of resetting them.

    Attributes:
        quit (bool): Flag to indicate if the game should quit.
        screen (pygame.Surface): The game screen.
        stack (list): A stack to keep track of the menu screens.
    """

    def __init__(self):
        self.quit = False
        self.screen = pygame.display.get_surface()
        self.stack = []
        self.stack.append(Main_Menu(self.stack))  # Start with the main menu screen.

    def update(self, clock):
        """
        Update the menu.

        Args:
            clock (pygame.time.Clock): The game clock.

        Returns:
            bool: True if the game should continue, False if the game should quit.
        """
        if self.quit:
            return False

        self.stack[-1].update(
            clock
        )  # Update the current menu screen. This will effectively pause all other screens in the stack, and not waste resources on them.

        for event in pygame.event.get():  # Process events
            if event.type == pygame.QUIT:  # Check if the user wants to quit (by closing the window)
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if the user clicked on the screen
                if event.button == 1:
                    self.stack[-1].on_click(
                        event.pos
                    )  # Pass the click position to the current menu screen that will handle it.
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.stack[-1].on_key(
                    event.key, event.type == pygame.KEYDOWN
                )  # Pass any key press or release to the current menu screen that will handle it.

        return True

    def draw(self):
        """
        Draw the current menu screen.
        """
        self.stack[-1].draw()

    def back(self):
        """
        Go back to the previous menu screen.
        This method is legacy and is not implemented in every class, depending on the imports and the need.
        """
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            self.quit = True


class Main_Menu(MenuFactory):
    """
    The main menu screen class.

    Contains buttons to start the game, open the resolution custom menu, and quit the game.

    Attributes:
        stack (list): A stack to keep track of the menu screens.
    """

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
        """
        Open the resolution custom menu screen.
        """
        self.stack.append(Resolution_Custom(self.stack))

    def start_game(self):
        """
        Start the game.
        """
        self.stack.append(Game(self.stack))
