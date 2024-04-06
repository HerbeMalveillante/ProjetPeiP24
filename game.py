import pygame
from constants import HEIGHT, LABYRINTH_RESOLUTION, WHITE, WIDTH, BUTTON_COLOR
from labyrinth import Labyrinth
from character import Character, Point, Enemy
from menufactory import MenuFactory, Text, Button
import random


class Game(MenuFactory):
    def __init__(self, stack):

        super().__init__()

        self.stack = stack
        self.STAIRS_IMAGE = pygame.image.load("stairs.png").convert()
        self.STAIRS_IMAGE = pygame.transform.scale(
            self.STAIRS_IMAGE, (int(LABYRINTH_RESOLUTION * 0.7), int(LABYRINTH_RESOLUTION * 0.7))
        )

        self.screen = pygame.display.get_surface()

        self.debug_text = Text(self.screen.get_width() - 300, 20, WHITE, "LoremIpsum")
        self.elements.add(self.debug_text)
        self.debug_text_2 = Text(self.screen.get_width() - 300, 50, WHITE, "LoremIpsum")
        self.elements.add(self.debug_text_2)
        self.quit_button = Button(
            self.screen.get_width() - 100, self.screen.get_height() - 50, 80, 30, BUTTON_COLOR, "Quitter", self.back
        )
        self.buttons.add(self.quit_button)

        self.level = 0
        self.total_points = 0

        self.load_level()

    def load_level(self):
        # On génère un nouveau labyrinthe (de taille différente éventuellement)
        # On place les ennemis
        # On place les points
        # On place la sortie
        # etc
        self.labyrinth = Labyrinth(
            (16 + self.level * 2, 16 + self.level * 2), "dead-end-filling", "recursive-backtracking", 0.1
        )
        while not self.labyrinth.generation_data["is_generated"]:
            self.labyrinth.generate_step()

        self.lab_layer = self.labyrinth.get_image()

        self.game_layer = pygame.Surface(
            (self.lab_layer.get_size()[0], self.lab_layer.get_size()[1]), pygame.SRCALPHA, 32
        )

        self.point_count = 0
        self.points_to_get = (self.labyrinth.width * self.labyrinth.height // 100 * 3) // 2

        self.points = []
        self.enemies = []
        self.character = Character(0, self.labyrinth, self)

        enemies_count = self.labyrinth.width * self.labyrinth.height // 100
        for e in range(enemies_count):
            position_valid = False
            while not position_valid:
                position = random.randint(0, self.labyrinth.width * self.labyrinth.height - 1)
                if (
                    position not in [e.pos for e in self.enemies]
                    and self.labyrinth.MD(self.character.pos, position) > 10
                ):
                    position_valid = True
            self.enemies.append(Enemy(position, self.labyrinth, self.character))
        points_count = enemies_count * 3
        for p in range(points_count):
            position_valid = False
            while not position_valid:
                position = random.randint(1, self.labyrinth.width * self.labyrinth.height - 2)
                if position not in [p.pos for p in self.points]:
                    position_valid = True
            self.points.append(Point(position, self.labyrinth))

    def update(self, clock):

        self.debug_text.update_text(f"Points : {self.point_count}/{self.points_to_get}")
        self.debug_text_2.update_text(f"Level : {self.level}")
        for e in self.enemies:
            e.update()
        self.character.update()
        if self.points_to_get <= self.point_count:
            stairs_size = self.STAIRS_IMAGE.get_size()[0]
            offset = (LABYRINTH_RESOLUTION - stairs_size) // 2
            stairs_coordinates = self.labyrinth.id_to_coord(self.labyrinth.width * self.labyrinth.height - 1)
            stairs_x = stairs_coordinates[0] * LABYRINTH_RESOLUTION + offset
            stairs_y = stairs_coordinates[1] * LABYRINTH_RESOLUTION + offset
            self.lab_layer.blit(self.STAIRS_IMAGE, (stairs_x, stairs_y))
        clock.tick(60)

    def draw(self):

        # Background : labyrinthe
        labyrinth_image_height = self.lab_layer.get_size()[1]
        displayable_height = HEIGHT - 40
        ratio = displayable_height / labyrinth_image_height
        labyrinth_image = pygame.transform.scale(
            self.lab_layer, (int(ratio * self.lab_layer.get_size()[0]), displayable_height)
        )

        # On la dessine à l'écran
        self.screen.blit(labyrinth_image, (20, 20))

        # Game layer
        self.game_layer.fill((0, 0, 0, 0))

        # Points
        for p in self.points:
            p_image = p.draw()
            p_x = p.local_x * LABYRINTH_RESOLUTION
            p_y = p.local_y * LABYRINTH_RESOLUTION
            self.game_layer.blit(p_image, (p_x, p_y))

        for e in self.enemies:
            e_image = e.draw()
            e_coordinates = self.labyrinth.id_to_coord(e.pos)
            e_x = e_coordinates[0] * LABYRINTH_RESOLUTION
            e_y = e_coordinates[1] * LABYRINTH_RESOLUTION
            self.game_layer.blit(e_image, (e_x, e_y))

        # Character
        character_image = self.character.draw()
        character_coordinates = self.labyrinth.id_to_coord(self.character.pos)
        character_x = character_coordinates[0] * LABYRINTH_RESOLUTION
        character_y = character_coordinates[1] * LABYRINTH_RESOLUTION
        self.game_layer.blit(character_image, (character_x, character_y))

        game_layer_image = pygame.transform.scale(
            self.game_layer, (int(ratio * self.game_layer.get_size()[0]), displayable_height)
        )
        self.screen.blit(game_layer_image, (20, 20))

        super().draw()

    def on_key(self, key, down):
        """
        the down argument indicates if the key has been pressed.
        For held keys, use pygame.keys.get_pressed() instead.
        """
        if down:
            if key == pygame.K_UP:
                if self.labyrinth.id_to_coord(self.character.pos)[1] > 0:
                    self.character.move("up")
            elif key == pygame.K_DOWN:
                if self.labyrinth.id_to_coord(self.character.pos)[1] < self.labyrinth.height - 1:
                    self.character.move("down")
            elif key == pygame.K_LEFT:
                if self.labyrinth.id_to_coord(self.character.pos)[0] > 0:
                    self.character.move("left")
            elif key == pygame.K_RIGHT:
                if self.labyrinth.id_to_coord(self.character.pos)[0] < self.labyrinth.width - 1:
                    self.character.move("right")

    def back(self):
        self.stack.pop()

    def lose(self):
        self.stack.append(
            EndGameScreen(
                self.stack, ["Vous avez perdu !", f"Niveau : {self.level}", f"Points : {self.total_points}"], self
            )
        )
        self.total_points = 0


class EndGameScreen(MenuFactory):

    def __init__(self, stack, gamedata, game):
        super().__init__()

        self.GAME = game

        last_y = 0
        for i in range(len(gamedata)):
            self.elements.add(Text(WIDTH / 2 - 90, 10 + i * 40, (255, 255, 255), gamedata[i]))
            last_y = 10 + i * 40

        self.buttons.add(
            Button(
                WIDTH / 2 - 90,
                last_y + 60,
                180,
                30,
                BUTTON_COLOR,
                "Rejouer",
                self.replay,
            )
        )

        self.buttons.add(
            Button(
                WIDTH / 2 - 90,
                last_y + 100,
                180,
                30,
                BUTTON_COLOR,
                "Menu principal",
                self.doubleBack,
            )
        )

        # self.elements.add(Text(WIDTH / 2 - 90, 10, (255, 255, 255), gamedata))

    def replay(self):
        self.GAME.level = 0
        self.GAME.load_level()
        self.GAME.stack.pop()

    def doubleBack(self):
        self.GAME.back()
        self.GAME.back()

    def back(self):

        self.GAME.back()
