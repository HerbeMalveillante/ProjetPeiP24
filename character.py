import pygame
import constants
import time


class Character(pygame.sprite.Sprite):

    def __init__(self, pos, labyrinth, game):
        super().__init__()

        self.labyrinth = labyrinth
        self.pos = pos
        self.game = game
        self.size = constants.LABYRINTH_RESOLUTION

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.has_changed = True

    def update(self):
        pass

    def draw(self):
        # Draw a circle on a new surface and return it
        if self.has_changed:
            self.image.fill((0, 0, 0, 0))

            pygame.draw.circle(
                self.image,
                constants.CHARACTER_COLOR,
                (self.size // 2, self.size // 2),
                self.size // 2 - constants.LABYRINTH_RESOLUTION // 4,
            )

            self.has_changed = False

        return self.image

    def move(self, direction):
        """
        direction: str<"up"|"down"|"left"|"right">
        moves are sanitized in the game class to avoid out of bounds moves.
        """

        if direction == "up":
            new_pos = self.pos - self.labyrinth.width
        elif direction == "down":
            new_pos = self.pos + self.labyrinth.width
        elif direction == "left":
            new_pos = self.pos - 1
        elif direction == "right":
            new_pos = self.pos + 1
        else:
            raise ValueError(f"Invalid direction: {direction}")
            exit()

        if not self.labyrinth.can_move(self.pos, new_pos):
            return

        enemies_pos = [e.pos for e in self.game.enemies]
        if new_pos in enemies_pos:
            self.lose()
            return

        points_pos = [p.pos for p in self.game.points]
        if new_pos in points_pos:
            self.game.points = [p for p in self.game.points if p.pos != new_pos]
            self.game.point_count += 1

        self.pos = new_pos

    def lose(self):
        print("You lose")
        self.game.back()


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, labyrinth, character):
        super().__init__()
        self.labyrinth = labyrinth
        self.character = character
        self.pos = pos
        self.size = constants.LABYRINTH_RESOLUTION

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.has_changed = True

        self.last_moved = time.time()

    def update(self):
        if time.time() - self.last_moved > 1:
            # path = self.labyrinth.resolve_recursive_backtracking(self.pos, self.character.pos)
            path = self.labyrinth.resolve_a_star(self.pos, self.character.pos)
            if len(path) < 2:
                self.character.lose()
            elif path:
                self.pos = path[1]
            self.last_moved = time.time()

    def draw(self):
        # Draw a circle on a new surface and return it
        if self.has_changed:
            self.image.fill((0, 0, 0, 0))

            pygame.draw.circle(
                self.image,
                constants.ENEMIES_COLOR,
                (self.size // 2, self.size // 2),
                self.size // 2 - constants.LABYRINTH_RESOLUTION // 4,
            )

            self.has_changed = False

        return self.image


class Point(pygame.sprite.Sprite):

    def __init__(self, pos, labyrinth):

        super().__init__()
        self.pos = pos
        self.local_x, self.local_y = labyrinth.id_to_coord(self.pos)
        self.image = pygame.Surface(
            (constants.LABYRINTH_RESOLUTION, constants.LABYRINTH_RESOLUTION), pygame.SRCALPHA, 32
        )
        self.rect = self.image.get_rect()

        self.animation = 0
        self.animation_count = 0
        self.width = 0

        self.labyrinth = labyrinth

    def draw(self):

        self.image.fill((0, 0, 0, 0))

        if self.animation > 120:
            self.animation = 0
            self.animation_count += 1
            self.width = 0

        if self.animation < 60:
            self.animation += 1
            self.width += 1
        else:
            self.animation += 1
            self.width -= 1

        center = constants.LABYRINTH_RESOLUTION // 2 - self.width // 2

        rect = pygame.Rect(center, 0, max(1, self.width), constants.LABYRINTH_RESOLUTION)
        rect.scale_by_ip(0.7, 0.7)

        color = constants.POINTS_COLOR if self.animation_count % 2 == 0 else constants.POINTS_COLOR_2

        pygame.draw.ellipse(
            self.image,
            color,
            rect,
        )

        return self.image
