import pygame
import constants
import time


class Character(pygame.sprite.Sprite):
    """
    Represents the character in the game.

    This class inherits from the pygame.sprite.Sprite class, which is used to create sprites in Pygame.
    This inheritance is useful because it provides boilerplate code to handle the drawing, updating and positioning of the character sprite, as well as performance optimizations.
    All the other classes in this module also inherit from the pygame.sprite.Sprite class for the same reasons.

    Attributes:
        pos (int): The current position of the character in the labyrinth.
        labyrinth (Labyrinth): The labyrinth object.
        game (Game): The game object.
        size (int): The size of the character sprite. It is the same as the "labyrinth resolution" constant which holds the size of the labyrinth cells.
        image (Surface): The surface representing the character sprite.
        has_changed (bool): Flag indicating if the character sprite has changed. Used to avoid redrawing the sprite every frame.
    """

    def __init__(self, pos, labyrinth, game):
        super().__init__()

        self.labyrinth = labyrinth
        self.pos = pos  # The character's position in the labyrinth is represented by a single integer, which is the index of the cell in the labyrinth.
        self.game = game
        self.size = constants.LABYRINTH_RESOLUTION

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32)
        self.has_changed = True

    def update(self):
        """
        Update the character's state.

        This method is called every frame to check for collisions with enemies.
        This method is useful to detect collisions immediately, because the enemies update method is only called every second.
        """
        enemies = self.game.enemies
        for enemy in enemies:
            if self.pos == enemy.pos:
                self.lose()

    def draw(self):
        """
        Draw the character sprite.

        Returns:
            Surface: The surface representing the character sprite.
        """
        if (
            self.has_changed
        ):  # We only redraw the character sprite if it has changed. This optimization is not strictly necessary, but it's good practice to have it in place in case we want to add animations later on.
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
        Move the character in the specified direction.

        This method also handles collisions with points and the end of the labyrinth, which do not need to be checked every frame.

        Args:
            direction (str): The direction to move the character. Can be "up", "down", "left", or "right".

        Raises:
            ValueError: If an invalid direction is provided.
        """
        if direction == "up":
            new_pos = (
                self.pos - self.labyrinth.width
            )  # The character's position is stored as the index of the cell it's in.
        elif direction == "down":
            new_pos = self.pos + self.labyrinth.width
        elif direction == "left":
            new_pos = self.pos - 1
        elif direction == "right":
            new_pos = self.pos + 1
        else:
            raise ValueError(f"Invalid direction: {direction}")
            exit()

        if not self.labyrinth.can_move(
            self.pos, new_pos
        ):  # We check if the character can move to the new position. We already have this method in the Labyrinth class for various other uses.
            return

        points_pos = [p.pos for p in self.game.points]
        if new_pos in points_pos:
            self.game.points = [p for p in self.game.points if p.pos != new_pos]
            self.game.point_count += 1
            self.game.total_points += 1

        end_pos = self.labyrinth.end
        if new_pos == end_pos:
            points_to_get = self.game.points_to_get
            if self.game.point_count >= points_to_get:
                self.game.level += 1
                self.game.load_level()

        self.pos = new_pos

    def lose(self):
        """
        Handle the character losing the game.
        """
        print("You lose")
        self.game.lose()


class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy in the game.

    Attributes:
        pos (int): The current position of the enemy in the labyrinth.
        labyrinth (Labyrinth): The labyrinth object.
        character (Character): The character object.
        size (int): The size of the enemy sprite.
        image (Surface): The surface representing the enemy sprite.
        has_changed (bool): Flag indicating if the enemy sprite has changed.
        last_moved (float): The time when the enemy last moved.
    """

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
        """
        Update the enemy's state.

        This method is called every frame to update the enemy's position and behavior.
        """
        if time.time() - self.last_moved > 1:  # The enemies move every second in the game loop
            path = self.labyrinth.resolve_a_star(self.pos, self.character.pos)
            if len(path) < 2:
                self.character.lose()
            elif path:
                self.pos = path[1]
            self.last_moved = time.time()

    def draw(self):
        """
        Draw the enemy sprite.

        Returns:
            Surface: The surface representing the enemy sprite.
        """
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
    """
    Represents a point in the game.

    Attributes:
        pos (int): The position of the point in the labyrinth.
        local_x (int): The x-coordinate of the point in the labyrinth.
        local_y (int): The y-coordinate of the point in the labyrinth.
        image (Surface): The surface representing the point sprite.
        rect (Rect): The rectangle representing the point sprite.
        animation (int): The current animation frame of the point sprite.
        animation_count (int): The number of times the point sprite has animated.
        width (int): The width of the point sprite.
        labyrinth (Labyrinth): The labyrinth object.
    """

    def __init__(self, pos, labyrinth):
        super().__init__()
        self.pos = pos
        self.local_x, self.local_y = labyrinth.id_to_coord(
            self.pos
        )  # The position is also stored as the x and y coordinates of the cell in the grid, to be later used in the Game class.
        self.image = pygame.Surface(
            (constants.LABYRINTH_RESOLUTION, constants.LABYRINTH_RESOLUTION), pygame.SRCALPHA, 32
        )
        self.rect = self.image.get_rect()

        self.animation = 0
        self.animation_count = 0
        self.width = 0

        self.labyrinth = labyrinth

    def draw(self):
        """
        Draw the point sprite.

        Returns:
            Surface: The surface representing the point sprite.
        """
        self.image.fill((0, 0, 0, 0))

        if self.animation > 120:  # The point sprite animation lasts for 120 frames.
            self.animation = 0
            self.animation_count += 1
            self.width = 0

        if self.animation < 60:  # The point is animated by increasing and decreasing its width.
            self.animation += 1
            self.width += 1
        else:
            self.animation += 1
            self.width -= 1

        center = constants.LABYRINTH_RESOLUTION // 2 - self.width // 2

        rect = pygame.Rect(
            center, 0, max(1, self.width), constants.LABYRINTH_RESOLUTION
        )  # We center the point sprite in the cell and draw it with the current width. We also make sure the width is at least 1 pixel.
        rect.scale_by_ip(0.7, 0.7)  # We scale the rectangle to make the point sprite look better.

        color = (
            constants.POINTS_COLOR if self.animation_count % 2 == 0 else constants.POINTS_COLOR_2
        )  # We alternate the color of the point sprite every time it animates, to give the illusion of the "coin" having two sides.

        pygame.draw.ellipse(
            self.image,
            color,
            rect,
        )

        return self.image
