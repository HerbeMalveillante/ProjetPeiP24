import pygame
from constants import WIDTH, HEIGHT, BUTTON_COLOR
from labyrinth import Labyrinth


class Menu:
    def __init__(self):

        self.quit = False
        # load the customFont.ttf file
        font_file = "customFont.ttf"
        self.font = pygame.font.Font(font_file, 16)
        self.font_big = pygame.font.Font(font_file, 32)
        self.screen = pygame.display.get_surface()

        self.stack = [Main_Menu(self)]

    def update(self):

        if self.quit:
            return False

        self.stack[-1].update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.stack[-1].on_click(event.pos)
        return True

    def draw(self):
        self.stack[-1].draw()

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            self.quit = True


class MenuFactory:
    def __init__(self, parent):
        self.parent = parent
        self.buttons = pygame.sprite.Group()
        self.elements = pygame.sprite.Group()

    def update(self):
        for el in self.elements:
            el.update()

    def draw(self):
        for el in self.elements:
            el.draw()
        for el in self.buttons:
            el.draw()

    def on_click(self, pos):
        # Create a virtual sprite to check for collisions
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = pygame.Rect(pos, (1, 1))

        # return the first button that collides with the mouse
        clicked = pygame.sprite.spritecollideany(mouse_sprite, self.buttons)

        if clicked and clicked.function:
            clicked.function()


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

        self.buttons.add(Button(self, WIDTH / 2 - 90, 93, 180, 30, BUTTON_COLOR, "Jouer", None))

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


class Resolution(MenuFactory):
    """
    Cette classe permet d'afficher la génération, puis la résolution du labyrinthe.
    On aura un autre menu entre le menu principal et celui-ci, qui permettra de choisir les options de génération et de résolution qui seront passés en paramètres.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.labyrinth = Labyrinth(self, (100, 100), "dead-end-filling", "recursive-backtracking", 0)

    def update(self):
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


class Game:
    def __init__(self, parent):
        self.parent = parent

    def update(self):
        pass

    def draw(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, parent, x, y, width, height, color, text, function):
        super().__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.function = function
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.font = self.parent.parent.font
        self.text_render = self.font.render(text, 0, (255, 255, 255))
        self.image.blit(
            self.text_render,
            (
                width / 2 - self.text_render.get_width() / 2,
                height / 2 - self.text_render.get_height() / 2,
            ),
        )

    def draw(self):
        self.parent.parent.screen.blit(self.image, (self.x, self.y))


class Text(pygame.sprite.Sprite):

    def __init__(self, parent, x, y, color, text):
        super().__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.font = self.parent.parent.font_big
        self.text_render = self.font.render(text, 0, color)

        self.image = self.text_render
        self.rect = self.image.get_rect()

    def draw(self):
        self.parent.parent.screen.blit(self.image, (self.x, self.y))
