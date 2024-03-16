import pygame
from constants import HEIGHT, LABYRINTH_RESOLUTION, WHITE
from labyrinth import Labyrinth
from character import Character, Point, Enemy
from menufactory import MenuFactory, Text


class Game(MenuFactory):
    def __init__(self, parent):

        super().__init__(parent)

        self.labyrinth = Labyrinth(self, (16, 16), "dead-end-filling", "recursive-backtracking", 0.1)
        while not self.labyrinth.generation_data["is_generated"]:
            self.labyrinth.generate_step()

        screen = pygame.display.get_surface()

        self.debug_text = Text(self, screen.get_width() - 300, 20, WHITE, "LoremIpsum")
        self.elements.add(self.debug_text)

        self.character = Character(0, self.labyrinth)

        self.lab_layer = self.labyrinth.get_image()
        self.game_layer = pygame.Surface(
            (self.lab_layer.get_size()[0], self.lab_layer.get_size()[1]), pygame.SRCALPHA, 32
        )

        self.points = []
        self.enemies = []

        self.points.append(Point(5, self.labyrinth))
        self.enemies.append(Enemy(10, self.labyrinth, self.character))

    def update(self, clock):
        point = self.points[0]
        anim, anim_count, width = point.animation, point.animation_count, point.width
        self.debug_text.update_text(f"anim: {anim}\nanim_count: {anim_count}\nwidth: {width}")
        for e in self.enemies:
            e.update()
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
        self.parent.parent.screen.blit(labyrinth_image, (20, 20))

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
        self.parent.parent.screen.blit(game_layer_image, (20, 20))

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
