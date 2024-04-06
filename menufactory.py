import pygame
import constants


class MenuFactory:
    """
    A class representing a menu factory.

    The menu factory is the base class for all menu screens in the game.
    It implements basic features such as updating, drawing, handling mouse clicks, and handling key events.
    Adding new UI elements to menus is done by adding them to the 'buttons' and 'elements' groups.

    Attributes:
    - buttons (pygame.sprite.Group): A group of buttons in the menu.
    - elements (pygame.sprite.Group): A group of elements in the menu.
    """

    def __init__(self):
        """
        Initialize the MenuFactory object.

        The buttons and elements groups are Pygame Group objects that allow for easy updating and drawing.
        Lists could be used instead but Pygame Groups provide additional functionality and are more performant in this context.
        """
        self.buttons = (
            pygame.sprite.Group()
        )  # Holds the buttons in the menu. Is separated from elements to handle click events.
        self.elements = pygame.sprite.Group()  # Holds non-interactable elements in the menu.

    def update(self, clock):
        """
        Update the elements in the menu.

        Parameters:
        - clock: The pygame clock object.
        """
        for el in self.elements:
            el.update()

    def draw(self):
        """
        Draw the elements and buttons in the menu.
        """
        for el in self.elements:
            el.draw()
        for el in self.buttons:
            el.draw()

    def on_click(self, pos):
        """
        Handle the click event in the menu.

        Parameters:
        - pos: The position of the mouse click.
        """
        # Create a virtual sprite to check for collisions
        # This method is very useful to avoid having to manually check for collisions between the mouse and the buttons.
        # It requires all the objects involved to be Pygame sprites, but it's a small price to pay for the convenience it provides.
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(pos, (1, 1))  # The virtual sprite is a single pixel at the mouse position

        # return the first button that collides with the mouse
        # This uses the spritecollideany method from Pygame to check for collisions between the mouse sprite and the buttons,
        # and returns the first button that collides with the mouse.
        clicked = pygame.sprite.spritecollideany(mouse_sprite, self.buttons)

        if clicked and clicked.function:  # If a button was clicked and it has a function
            clicked.function()  # Call the button's function

    def on_key(self, key, down):
        """
        Handle the key event in the menu.

        This method is empty by default, but can be overridden in subclasses to handle key events, such as in the game screen to move the character.

        Parameters:
        - key: The key that was pressed or released.
        - down: A boolean indicating whether the key was pressed (True) or released (False).
        """
        pass


class Button(pygame.sprite.Sprite):
    """
    A class representing a button in the menu.

    Attributes:
    - x (int): The x-coordinate of the button.
    - y (int): The y-coordinate of the button.
    - width (int): The width of the button.
    - height (int): The height of the button.
    - color (tuple): The color of the button.
    - text (str): The text displayed on the button.
    - function (function): The function to be called when the button is clicked.
    - rect (pygame.Rect): The rectangle representing the button.
    - image (pygame.Surface): The image of the button.
    - font (pygame.font.Font): The font used for the button text.
    - text_render (pygame.Surface): The rendered text of the button.
    - screen (pygame.Surface): The screen surface.
    """

    def __init__(self, x, y, width, height, color, text, function):
        """
        Initialize the Button object.

        Parameters:
        - x (int): The x-coordinate of the button.
        - y (int): The y-coordinate of the button.
        - width (int): The width of the button.
        - height (int): The height of the button.
        - color (tuple): The color of the button.
        - text (str): The text displayed on the button.
        - function (function): The function to be called when the button is clicked.
        """
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color  # The background color of the button. The text color is always white.
        self.text = text
        self.function = function  # The function to be called when the button is clicked.
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.font = (
            constants.font
        )  # The font is cached in the constants module for easy access : loading files from disk is slow.
        self.text_render = self.font.render(text, 0, (255, 255, 255))
        self.image.blit(
            self.text_render,
            (
                width / 2 - self.text_render.get_width() / 2,
                height / 2 - self.text_render.get_height() / 2,
            ),
        )  # Center the text on the button.

    def draw(self):
        """
        Draw the button on the screen.
        """
        self.screen.blit(self.image, (self.x, self.y))


class Text(pygame.sprite.Sprite):
    """
    A class representing a text element in the menu.

    Attributes:
    - x (int): The x-coordinate of the text element.
    - y (int): The y-coordinate of the text element.
    - color (tuple): The color of the text.
    - text (str): The text to be displayed.
    - font (pygame.font.Font): The font used for the text.
    - text_render (pygame.Surface): The rendered text.
    - image (pygame.Surface): The image of the text element.
    - rect (pygame.Rect): The rectangle representing the text element.
    - screen (pygame.Surface): The screen surface.
    """

    def __init__(self, x, y, color, text):
        """
        Initialize the Text object.

        Parameters:
        - x (int): The x-coordinate of the text element.
        - y (int): The y-coordinate of the text element.
        - color (tuple): The color of the text.
        - text (str): The text to be displayed.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.font = constants.font_big  # The font is cached in the constants module for easy access.
        self.text_render = self.font.render(text, 0, color)

        self.image = self.text_render
        self.rect = self.image.get_rect()

        self.screen = pygame.display.get_surface()

    def update_text(self, text):
        """
        Update the text of the text element.

        This is very useful when we need to display dynamic text, such as the score in the game or statistics in the custom resolution menu.

        Parameters:
        - text (str): The new text to be displayed.
        """
        self.text = text
        self.text_render = self.font.render(text, 0, self.color)
        self.image = self.text_render
        self.rect = self.image.get_rect()

    def draw(self):
        """
        Draw the text element on the screen.
        """
        self.screen.blit(self.image, (self.x, self.y))
