import pygame
from constants import HEIGHT, LABYRINTH_RESOLUTION, WHITE, WIDTH, BUTTON_COLOR
from labyrinth import Labyrinth
from character import Character, Point, Enemy
from menufactory import MenuFactory, Text, Button
import random


class Game(MenuFactory):
    """
    The Game class represents the main game screen.

    It inherits from the MenuFactory class, which handles the boilerplate for managing the UI elements.

    Parameters:
    - stack (list): A list representing the screen stack. This is used to navigate between screens.

    Attributes:
    - stack (list): A list representing the screen stack.
    - STAIRS_IMAGE (pygame.Surface): The image of the stairs.
    - screen (pygame.Surface): The game screen.
    - debug_text (Text): The debug text object.
    - debug_text_2 (Text): The second debug text object.
    - quit_button (Button): The quit button object.
    - level (int): The current level of the game.
    - total_points (int): The total points collected in the game.
    - labyrinth (Labyrinth): The labyrinth object.
    - lab_layer (pygame.Surface): The labyrinth layer.
    - game_layer (pygame.Surface): The game layer.
    - point_count (int): The number of points collected in the current level.
    - points_to_get (int): The total number of points to collect to unlock the stairs.
    - points (list): A list of Point objects.
    - enemies (list): A list of Enemy objects.
    - character (Character): The character object.
    """

    def __init__(self, stack):
        """
        Initialize the Game object.

        Parameters:
        - stack (list): A list representing the screen stack.
        """
        super().__init__()

        self.stack = stack
        self.STAIRS_IMAGE = pygame.image.load(
            "stairs.png"
        ).convert()  # The convert method is used to optimize the image for faster blitting.
        self.STAIRS_IMAGE = pygame.transform.scale(
            self.STAIRS_IMAGE, (int(LABYRINTH_RESOLUTION * 0.7), int(LABYRINTH_RESOLUTION * 0.7))
        )  # Resize the image to avoid overlapping with the walls and make it fit in the cell.

        self.screen = pygame.display.get_surface()

        # Add two debug text elements to display information about the game state.
        # Adding them to the elements group ensures they are updated and drawn automatically.
        self.debug_text = Text(self.screen.get_width() - 300, 20, WHITE, "LoremIpsum")
        self.elements.add(self.debug_text)
        self.debug_text_2 = Text(self.screen.get_width() - 300, 50, WHITE, "LoremIpsum")
        self.elements.add(self.debug_text_2)

        # Add a quit button to exit the game. It calls the back method when clicked.
        self.quit_button = Button(
            self.screen.get_width() - 100, self.screen.get_height() - 50, 80, 30, BUTTON_COLOR, "Quitter", self.back
        )
        self.buttons.add(self.quit_button)

        self.level = (
            0  # The current level of the game. It is used to generate the labyrinth, points and enemies procedurally.
        )
        self.total_points = 0  # The total points collected in the game. It is used to calculate the final score.

        self.load_level()  # Load the first level of the game.

    def load_level(self):
        """
        Load a new level in the game.

        This method generates a new labyrinth, points, enemies, and character for the game.
        """

        # Generate a new labyrinth for the game using the level as a parameter.
        # The size of the labyrinth increases by 2 for each level, starting from 16x16.
        # The generation algorithm is "dead-end-filling". The solving algorithm is pointless in this context.
        # The looping factor is set to 0.1 to create a fair amount of loops in the labyrinth.
        # The more loops there are, the easier it is to navigate the labyrinth without getting stuck between enemies.
        self.labyrinth = Labyrinth(
            (16 + self.level * 2, 16 + self.level * 2), "dead-end-filling", "recursive-backtracking", 0.1
        )

        # We don't really want to see the generation process, so we do it all at once.
        # There is no noticeable performance issue with this approach, even for larger labyrinths.
        while not self.labyrinth.generation_data["is_generated"]:
            self.labyrinth.generate_step()

        # We want to display the labyrinth separately from the game elements, so we create a separate layer for it.
        # We conveniently use the labyrinth's get_image method to get a surface representing the labyrinth.
        self.lab_layer = self.labyrinth.get_image()

        # We create a game layer to draw the points, enemies, and character on top of the labyrinth.
        # We use the same size as the labyrinth layer to ensure proper alignment.
        # We also make sure the game layer has an alpha channel for transparency.
        self.game_layer = pygame.Surface(
            (self.lab_layer.get_size()[0], self.lab_layer.get_size()[1]), pygame.SRCALPHA, 32
        )

        # Reset the point count for the new level.
        # The player needs to collect a certain number of points to unlock the stairs and progress to the next level.
        self.point_count = 0
        self.points_to_get = (self.labyrinth.width * self.labyrinth.height // 100 * 3) // 2

        # Create the points, enemies, and character for the new level.
        # Pygame Groups could be used to manage these objects more efficiently,
        # But the performance gains would be negligible for the current scale of the game.
        self.points = []
        self.enemies = []
        self.character = Character(0, self.labyrinth, self)

        # We want one enemy for every 100 cells in the labyrinth.
        enemies_count = self.labyrinth.width * self.labyrinth.height // 100
        for e in range(enemies_count):
            position_valid = False
            while not position_valid:
                # Generate a new random position for the enemy in the labyrinth.
                position = random.randint(0, self.labyrinth.width * self.labyrinth.height - 1)
                # Make sure the position is not already occupied by another enemy and is far enough from the character. We can use the Manhattan distance for this, as it is already implemented for the A* algorithm.
                if (
                    position not in [e.pos for e in self.enemies]
                    and self.labyrinth.MD(self.character.pos, position) > 10
                ):
                    position_valid = True
            # If all conditions are met, create a new enemy object and add it to the list.
            self.enemies.append(Enemy(position, self.labyrinth, self.character))

        # We want three points for every enemy in the labyrinth.
        points_count = enemies_count * 3
        for p in range(points_count):
            position_valid = False
            while not position_valid:
                # Make sure the position is not overlapping with the start or the end of the labyrinth.
                # This is not such a big deal for the enemies since they move around, but it's important for the points.
                position = random.randint(1, self.labyrinth.width * self.labyrinth.height - 2)
                if position not in [p.pos for p in self.points]:
                    # We don't want the points to overlap with each other either.
                    position_valid = True
            # If all conditions are met, create a new point object and add it to the list.
            self.points.append(Point(position, self.labyrinth))

    def update(self, clock):
        """
        Update the game state.

        Parameters:
        - clock (pygame.time.Clock): The game clock object.
        """

        # Update the debug text elements to display the current game state.
        # Here, we are displaying the number of points collected and the number of points needed to unlock the stairs, as well as the current level.
        self.debug_text.update_text(f"Points : {self.point_count}/{self.points_to_get}")
        self.debug_text_2.update_text(f"Level : {self.level}")
        for e in self.enemies:
            # Update the state of each enemy in the game
            e.update()
        self.character.update()  # Update the state of the character in the game.
        # If the player has collected enough coins to unlock the stairs, display them at the end of the labyrinth.
        if self.points_to_get <= self.point_count:
            stairs_size = self.STAIRS_IMAGE.get_size()[0]
            offset = (LABYRINTH_RESOLUTION - stairs_size) // 2
            stairs_coordinates = self.labyrinth.id_to_coord(self.labyrinth.width * self.labyrinth.height - 1)
            stairs_x = stairs_coordinates[0] * LABYRINTH_RESOLUTION + offset
            stairs_y = stairs_coordinates[1] * LABYRINTH_RESOLUTION + offset
            self.lab_layer.blit(self.STAIRS_IMAGE, (stairs_x, stairs_y))

        # Slow down the game loop to sixty frames per second.
        # This makes the game less framerate-dependant and ensures a consistent experience for the player.
        # The game logic is still updated every frame, but the rendering is limited to 60 FPS.
        # The game may be slowed down if the hardware cannot handle 60 FPS, but it cannot run faster than 60 FPS.
        clock.tick(60)

    def draw(self):
        """
        Draw the game screen.
        """

        # Calculate the maximum size of the labyrinth image that can fit in the game window.
        # This theoretically allows the game to be played on different screen sizes,
        # But this would require additional adjustments to the UI elements and scaling.
        labyrinth_image_height = self.lab_layer.get_size()[1]
        displayable_height = HEIGHT - 40
        ratio = displayable_height / labyrinth_image_height
        # Scale the labyrinth image to fit the game window.
        # This can cause the lines of the labyrinth to become invisible on high labyrinth sizes (>75x75).
        labyrinth_image = pygame.transform.scale(
            self.lab_layer, (int(ratio * self.lab_layer.get_size()[0]), displayable_height)
        )

        self.screen.blit(labyrinth_image, (20, 20))

        # Clear the game layer
        self.game_layer.fill((0, 0, 0, 0))

        # Draw the points, enemies, and character on the game layer.
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

        character_image = self.character.draw()
        character_coordinates = self.labyrinth.id_to_coord(self.character.pos)
        character_x = character_coordinates[0] * LABYRINTH_RESOLUTION
        character_y = character_coordinates[1] * LABYRINTH_RESOLUTION
        self.game_layer.blit(character_image, (character_x, character_y))

        # Draw the game layer on top of the labyrinth layer, with the same scaling factor to ensure alignment.
        game_layer_image = pygame.transform.scale(
            self.game_layer, (int(ratio * self.game_layer.get_size()[0]), displayable_height)
        )
        self.screen.blit(game_layer_image, (20, 20))

        # Draw the UI elements on top of the game screen.
        super().draw()

    def on_key(self, key, down):
        """
        Handle key events.

        Parameters:
        - key (int): The key code.
        - down (bool): Indicates if the key is pressed down.
        """

        # Handle the character movement
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
        """
        Go back to the previous screen.
        """
        self.stack.pop()

    def lose(self):
        """
        Handle the game over event.
        """

        # Add the End Game Screen to the screen stack with the game data, to display in the game over screen.
        self.stack.append(
            EndGameScreen(
                self.stack, ["Vous avez perdu !", f"Niveau : {self.level}", f"Points : {self.total_points}"], self
            )
        )
        self.total_points = 0


class EndGameScreen(MenuFactory):
    """
    The EndGameScreen class represents the end game screen.

    Parameters:
    - stack (list): A list representing the screen stack.
    - gamedata (list): A list of game data to display.
    - game (Game): The Game object.

    Attributes:
    - GAME (Game): The Game object.
    """

    def __init__(self, stack, gamedata, game):
        """
        Initialize the EndGameScreen object.

        Parameters:
        - stack (list): A list representing the screen stack. It is not used in this class but addded for consistency.
        - gamedata (list): A list of game data to display.
        - game (Game): The Game object.
        """
        super().__init__()

        self.GAME = game

        last_y = 0  # The last y position of the text elements, used to position the buttons correctly.
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
                self.doubleBack,  # This method is used to go back to the main menu. We need to go back once to reach the Game screen, then one more time to reach the Main Menu screen.
            )
        )

    def replay(self):
        """
        Restart the game.
        """
        self.GAME.level = 0
        self.GAME.load_level()
        self.GAME.stack.pop()  # We need to remove the EndGameScreen from the stack to display the Game screen again.

    def doubleBack(self):
        """
        Go back to the main menu.
        """
        self.GAME.back()
        self.GAME.back()

    def back(self):
        """
        Go back to the previous screen.
        """
        self.GAME.back()
