import pygame
import constants


class MenuFactory:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.elements = pygame.sprite.Group()

    def update(self, clock):
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

    def on_key(self, key, down):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text, function):
        super().__init__()
        self.screen = pygame.display.get_surface()
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
        self.font = constants.font
        self.text_render = self.font.render(text, 0, (255, 255, 255))
        self.image.blit(
            self.text_render,
            (
                width / 2 - self.text_render.get_width() / 2,
                height / 2 - self.text_render.get_height() / 2,
            ),
        )

    def draw(self):

        self.screen.blit(self.image, (self.x, self.y))


class Text(pygame.sprite.Sprite):

    def __init__(self, x, y, color, text):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.font = constants.font_big
        self.text_render = self.font.render(text, 0, color)

        self.image = self.text_render
        self.rect = self.image.get_rect()

        self.screen = pygame.display.get_surface()

    def update_text(self, text):
        self.text = text
        self.text_render = self.font.render(text, 0, self.color)
        self.image = self.text_render
        self.rect = self.image.get_rect()

    def draw(self):

        self.screen.blit(self.image, (self.x, self.y))
