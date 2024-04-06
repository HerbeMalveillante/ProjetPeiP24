import pygame
import time
import random
from constants import LABYRINTH_RESOLUTION, DRAW_CASE_NUMBERS, BUTTON_COLOR, LINE_WIDTH, font
import math


def generate_color(min, max, value):
    """
    Generate a RGB color on a gradient from red to green based on a value between min and max.
    This is used for the A* pathfinding algorithm to color the cells based on their fScore.
    This method works for any fScore values, which can be arbitrary depending on the implementation.
    It's also useful to display the differences more clearly when the fScore values are close to each other.
    It also allows for a grey color if min == max, which can happen if the fScore is constant for all cells (usually at the beginning of the algorithm).

    Parameters:
    - min (float): The minimum value of the range.
    - max (float): The maximum value of the range.
    - value (float): The value to generate the color for.

    Returns:
    - tuple: The RGB color tuple.
    """
    if value < min:
        value = min
    elif value > max:
        value = max

    # A division by zero is possible if min == max. In this case, we return a grey color.
    if min == max:
        return (128, 128, 128)

    green = int((value - min) / (max - min) * 255)
    red = 255 - green

    return (red, green, 0)


class Labyrinth(pygame.sprite.Sprite):
    """
    Represents a labyrinth object.

    Attributes:
        width (int): The width of the labyrinth in cells.
        height (int): The height of the labyrinth in cells.
        matrix (list): The matrix representation of the labyrinth.
        image (Surface): The surface representing the labyrinth.
        pathfinding_layer (Surface): The surface representing the pathfinding layer.
        rect (Rect): The rectangle representing the labyrinth.
        has_changed (bool): Flag indicating if the labyrinth has changed (useful for optimization purposes)
        walls (list): The list of walls in the labyrinth.
        start (int): The ID of the start cell. By default, it's the top-left cell.
        end (int): The ID of the end cell. By default, it's the bottom-right cell.
        generation_algorithm (str): The algorithm used for generating the labyrinth.
        resolution_algorithm (str): The algorithm used for solving the labyrinth.
        looping_factor (float): The factor for randomly removing walls after generation.
        generation_data (dict): The data for the labyrinth generation process.
        resolution_data (dict): The data for the labyrinth resolution process.

    """

    def __init__(self, size, generation_algorithm, resolution_algorithm, looping_factor):
        """
        Initializes a new instance of the Labyrinth class.

        Parameters:
        - size (tuple): The size of the labyrinth (width, height).
        - generation_algorithm (str): The algorithm to use for generating the labyrinth.
        - resolution_algorithm (str): The algorithm to use for resolving the labyrinth.
        - looping_factor (float): The factor for randomly removing walls after generation.
        """
        super().__init__()

        self.width = size[0]
        self.height = size[1]
        self.matrix = [[j + i * self.width for j in range(self.width)] for i in range(self.height)]

        # We want to create two separate surfaces for the labyrinth:
        # - The main labyrinth image, which will contain the walls and cells.
        # - The pathfinding layer, which will contain the pathfinding information
        # This allows for massive optimization, as the pathfinding layer does not change during the generation,
        # and the labyrinth image does not change during the resolution.
        self.image = pygame.Surface((self.width * LABYRINTH_RESOLUTION, self.height * LABYRINTH_RESOLUTION))
        self.pathfinding_layer = pygame.Surface(
            (self.width * LABYRINTH_RESOLUTION, self.height * LABYRINTH_RESOLUTION), pygame.SRCALPHA, 32
        )
        self.rect = self.image.get_rect()
        self.has_changed = True  # Flag indicating if the labyrinth has changed (useful for optimization purposes)

        self.walls = []

        self.start = 0
        self.end = self.width * self.height - 1

        self.generation_algorithm = generation_algorithm
        self.resolution_algorithm = resolution_algorithm

        self.looping_factor = looping_factor

        # The generation data contains all the information needed for the generation process.
        # This includes the current state of the generation, the stack of cells, the visited cells, the walls, etc.
        # Using a mutable type (dict) allows for easy access and modification of the data without the use of global variables or
        # multiple return values in functions.
        # Storing them directly as attributes of the Labyrinth object allows for easy access and modification from other parts of the code,
        # since the labyrinth object is passed around pretty much everywhere.

        # We start the generation process by setting the current cell to a random cell in the labyrinth.
        current = random.randint(0, self.width * self.height - 1)
        self.generation_data = {
            "is_generated": False,  # Flag indicating if the labyrinth has been generated.
            "start_time": time.perf_counter(),  # The time when the generation process started.
            "generation_time": 0,  # The total time taken to generate the labyrinth.
            "step": 0,  # The current step in the generation process.
            "action_count": 0,  # The total number of actions taken during the generation process.
            "stack": [current],  # The stack of cells used during the generation process.
            "visited": [current],  # The list of visited cells during the generation process.
            "wall_index": 0,  # The current index of the wall being processed.
            "perfect_wall_count": 0,  # The total number of walls in a perfect labyrinth.
        }

        if self.resolution_algorithm == "recursive-backtracking":
            self.resolution_data = {
                "is_solved": False,  # Flag indicating if the labyrinth has been solved.
                "start_time": time.perf_counter(),  # The time when the resolution process started.
                "resolution_time": 0,  # The total time taken to resolve the labyrinth.
                "setupDone": False,  # Flag indicating if the resolution process has been set up.
                "stack": [self.start],  # The stack of cells used during the resolution process.
                "banned": [],  # The list of banned cells during the resolution process.
                "visited": [],  # The list of visited cells during the resolution process.
                "total_move_count": 0,  # The total number of moves taken during the resolution process.
            }
        elif self.resolution_algorithm == "a-star":
            self.resolution_data = {
                "is_solved": False,  # Flag indicating if the labyrinth has been solved.
                "start_time": time.perf_counter(),  # The time when the resolution process started.
                "resolution_time": 0,  # The total time taken to resolve the labyrinth.
                "setupDone": False,  # Flag indicating if the resolution process has been set up.
                "openSet": [],  # The set of nodes to be evaluated.
                "cameFrom": {},  # The map of navigated nodes.
                "gScore": {},  # The map of cost from start along best known path.
                "fScore": {},  # The map of estimated total cost from start to goal through y.
                "path": [],  # The final path from start to end.
                "current": None,  # The current node being evaluated.
                "total_move_count": 0,  # The total number of moves taken during the resolution process.
            }

    def id_to_coord(self, id):
        """
        Converts a cell ID to its corresponding coordinates in the labyrinth.

        Parameters:
        - id (int): The cell ID.

        Returns:
        - tuple: The coordinates (x, y) of the cell.
        """
        return (id % self.width, id // self.width)

    def coord_to_id(self, x, y=None):
        """
        Converts coordinates to the corresponding cell ID in the labyrinth.

        Parameters:
        - x (int or tuple): The x-coordinate or the coordinates (x, y) of the cell.
        - y (int): The y-coordinate of the cell.

        Returns:
        - int: The cell ID.
        """
        if y is None:
            y = x[1]
            x = x[0]
        return y * self.width + x

    def is_adjacent(self, case_1, case_2):
        """
        Checks if two cells are adjacent to each other.

        Parameters:
        - case_1 (int): The ID of the first cell.
        - case_2 (int): The ID of the second cell.

        Returns:
        - bool: True if the cells are adjacent, False otherwise.
        """
        case_1, case_2 = min(case_1, case_2), max(
            case_1, case_2
        )  # Allows for the function to work with unordered arguments
        return case_1 in self.get_adjacent_cases(case_2)

    def get_adjacent_cases(self, case):
        """
        Gets the adjacent cells of a given cell.

        This do not take the walls into account, but allows for easy access to the adjacent cells when processing
        the cells that are next to the borders of the labyrinth.

        Parameters:
        - case (int): The ID of the cell.

        Returns:
        - list: A list of adjacent cell IDs.
        """
        adjacent = []
        if case % self.width != 0:
            adjacent.append(case - 1)
        if (case + 1) % self.width != 0:
            adjacent.append(case + 1)
        if case >= self.width:
            adjacent.append(case - self.width)
        if case < self.width * (self.height - 1):
            adjacent.append(case + self.width)

        return adjacent

    def add_wall(self, case_1, case_2):
        """
        Adds a wall between two adjacent cells.

        Parameters:
        - case_1 (int): The ID of the first cell.
        - case_2 (int): The ID of the second cell.

        Returns:
        - bool: True if the wall was added successfully, False otherwise.
        """
        if not self.is_adjacent(case_1, case_2):  # We can't add a wall between two non-adjacent cells
            print(f"Impossible d'ajouter un mur : les cases {case_1} et {case_2} ne sont pas adjacentes.")
            return False
        case_1, case_2 = min(case_1, case_2), max(
            case_1, case_2
        )  # Allows for the function to work with unordered arguments
        if (case_1, case_2) not in self.walls:  # We don't want to add the same wall twice
            self.walls.append((case_1, case_2))
            self.has_changed = True  # The labyrinth has changed, so we need to redraw it
            return True
        return False

    def remove_wall(self, case_1, case_2):
        """
        Removes a wall between two adjacent cells.

        Parameters:
        - case_1 (int): The ID of the first cell.
        - case_2 (int): The ID of the second cell.

        Returns:
        - bool: True if the wall was removed successfully, False otherwise.
        """
        case_1, case_2 = min(case_1, case_2), max(case_1, case_2)
        if (case_1, case_2) in self.walls:
            self.walls.remove((case_1, case_2))
            self.has_changed = True
            return True
        print(f"Il n'y a pas de mur entre les cases {case_1} et {case_2}.")
        return False

    def fill_with_walls(self):
        """
        Fills the labyrinth with walls.
        """
        for i in range(self.width * self.height):  # We iterate over all the cells in the labyrinth
            if i >= self.width * self.height - 1:
                continue
            localIterator = i % self.width  # We calculate the local iterator to know if we are at the end of a line
            # Horizontal
            if (i + 1) % self.width > localIterator:
                self.add_wall(i, i + 1)
            # Vertical
            if i + self.width < self.width * self.height:
                self.add_wall(i, i + self.width)

    def can_move(self, case_1, case_2):
        """
        Checks if it is possible to move from one cell to another.

        This method takes into account the walls in the labyrinth.

        Parameters:
        - case_1 (int): The ID of the first cell.
        - case_2 (int): The ID of the second cell.

        Returns:
        - bool: True if it is possible to move, False otherwise.
        """
        case1, case2 = min(case_1, case_2), max(
            case_1, case_2
        )  # Allows for the function to work with unordered arguments
        if not self.is_adjacent(case1, case2):  # We can't move between non-adjacent cells
            return False
        if (case1, case2) in self.walls:  # We can't move through walls
            return False
        return True

    def generate_step(self):
        """
        Performs a step in the labyrinth generation process.

        This method allows for the generation process to be performed step by step, which is useful for visualizing the generation process.
        This involves a pretty big refactoring of both the algorithms themselves, the way they are called, and the way they store and update their data.
        Since the variables in this function are "cleared" at each call, we need to store the data in the labyrinth object itself.

        Returns:
        - bool: True if the generation is complete, False otherwise.
        """
        if not self.generation_data["is_generated"]:

            if self.generation_algorithm == "dead-end-filling":
                if (
                    self.generation_data["step"] == 0
                ):  # We fill the labyrinth with walls to start the generation process
                    self.fill_with_walls()
                    self.generation_data["step"] = 1
                    print("Première étape terminée : remplissage des murs.")
                    return False  # We return False to indicate that the generation is not complete, but to keep the process going
                elif self.generation_data["step"] == 1:  # Dead-end filling

                    if len(self.generation_data["stack"]) == 0:  # We have finished the generation process
                        self.generation_data["step"] = 2  # We move to the next step
                        self.generation_data["perfect_wall_count"] = len(
                            self.walls
                        )  # We store the number of walls for the looping factor
                        print("Deuxième étape terminée : labyrinthe parfait généré.")
                        return False

                    else:
                        # The main part of the algorithm
                        current = self.generation_data["stack"][
                            -1
                        ]  # We get the current cell as the last cell in the stack (FILO)
                        adjacent_cases = self.get_adjacent_cases(current)
                        unvisited_adjacent_cases = [
                            case for case in adjacent_cases if case not in self.generation_data["visited"]
                        ]  # We don't want to visit the same cell twice

                        if len(unvisited_adjacent_cases) == 0:  # We have reached a dead end : we must backtrack
                            self.generation_data["stack"].pop()  # We remove the current cell from the stack
                            return False

                        next_case = random.choice(
                            unvisited_adjacent_cases
                        )  # If we can still move, we choose a random adjacent cell
                        self.remove_wall(
                            current, next_case
                        )  # and break the wall between the two cells to create a path
                        self.generation_data["visited"].append(next_case)  # We mark the cell as visited
                        self.generation_data["stack"].append(
                            next_case
                        )  # We add the cell to the stack (it will be picked as the current cell in the next iteration)
                        self.generation_data["action_count"] += 1  # We increment the action count for statistics

                elif self.generation_data["step"] == 2:  # looping factor

                    if self.looping_factor != 0:  # We only loop if the factor is not 0
                        for _ in range(
                            int(len(self.walls) * self.looping_factor)
                        ):  # The looping factor is a percentage of the total number of walls to be removed. Incidentally, this is also the number of iterations we will do.
                            wall = random.choice(self.walls)  # We choose a random wall
                            self.remove_wall(wall[0], wall[1])  # and remove it
                            self.generation_data["action_count"] += 1  # We increment the action count for statistics
                    self.generation_data["is_generated"] = True  # We have finished the generation process
                    self.generation_data["step"] = 3  # We move to the next step
                    print("Troisième et dernière étape terminée : murs aléatoires supprimés.")

                    return True

            else:
                print("L'algorithme de génération n'est pas reconnu.")  # We don't recognize the generation algorithm
                raise NotImplementedError  # We raise a NotImplementedError to indicate that the algorithm is not implemented

        self.generation_data["generation_time"] = (
            time.perf_counter() - self.generation_data["start_time"]
        )  # We update the generation time. This allows us to keep track of the time taken to generate the labyrinth, independently of the framerate.

    def resolve_step(self):
        """
        Performs a step in the labyrinth resolution process.
        """
        if not self.resolution_data["is_solved"]:

            # We update the resolution time. This allows us to keep track of the time taken to resolve the labyrinth, independently of the framerate.
            self.resolution_data["resolution_time"] = time.perf_counter() - self.resolution_data["start_time"]

            if self.resolution_algorithm == "a-star":

                def h(case):
                    # We use the Manhattan distance as the heuristic function
                    return self.MD(case, self.end)

                def reconstruct_path(cameFrom, current):
                    # We reconstruct the path from the cameFrom map
                    totalPath = [current]
                    while current in cameFrom.keys():
                        current = cameFrom[current]
                        totalPath.append(current)
                    totalPath.reverse()  # We reverse the path to get the correct order
                    return totalPath

                # Initial setup of the A* algorithm : we set the start time, the openSet, the cameFrom map, the gScore and fScore maps, and the current cell

                if not self.resolution_data["setupDone"]:
                    self.resolution_data["start_time"] = time.perf_counter()
                    print("Initialisation de l'algorithme A*...")
                    self.resolution_data["openSet"] = [self.start]
                    self.resolution_data["cameFrom"] = {}

                    self.resolution_data["gScore"] = {}
                    for x in range(self.width * self.height):
                        self.resolution_data["gScore"][
                            x
                        ] = math.inf  # The gScore is initialized to infinity for all cells except the start cell
                    self.resolution_data["gScore"][self.start] = 0
                    self.resolution_data["fScore"] = {}
                    for x in range(self.width * self.height):
                        self.resolution_data["fScore"][
                            x
                        ] = math.inf  # The fScore is initialized to infinity for all cells except the start cell
                    self.resolution_data["fScore"][self.start] = h(self.start)

                    self.resolution_data["setupDone"] = True  # We have finished the setup

                    print("Initialisation terminée.")

                if len(self.resolution_data["openSet"]) > 0:  # We have cells to evaluate
                    self.resolution_data["current"] = min(
                        self.resolution_data["openSet"], key=lambda x: self.resolution_data["fScore"][x]
                    )  # We get the cell with the lowest fScore
                    if self.resolution_data["current"] == self.end:  # We have reached the end cell
                        print("Chemin trouvé.")

                        # Compute the final path
                        self.resolution_data["path"] = reconstruct_path(
                            self.resolution_data["cameFrom"], self.resolution_data["current"]
                        )

                        self.resolution_data["is_solved"] = True  # We have finished the resolution process
                        return True

                    self.resolution_data["openSet"].remove(
                        self.resolution_data["current"]
                    )  # We remove the current cell from the openSet
                    adjacent = self.get_adjacent_cases(self.resolution_data["current"])  # We get the adjacent cells
                    adjacent = [
                        a for a in adjacent if self.can_move(self.resolution_data["current"], a)
                    ]  # We filter the cells that can be moved to
                    for neighbor in adjacent:
                        tentative_gScore = (
                            self.resolution_data["gScore"][self.resolution_data["current"]] + 1
                        )  # We increment the gScore by 1
                        if tentative_gScore < self.resolution_data["gScore"][neighbor]:  # We have found a better path
                            self.resolution_data["cameFrom"][neighbor] = self.resolution_data[
                                "current"
                            ]  # We update the cameFrom map
                            self.resolution_data["gScore"][neighbor] = tentative_gScore  # We update the gScore
                            self.resolution_data["fScore"][neighbor] = tentative_gScore + h(
                                neighbor
                            )  # We update the fScore
                            if (
                                neighbor not in self.resolution_data["openSet"]
                            ):  # We add the neighbor to the openSet if it's not already there
                                self.resolution_data["openSet"].append(neighbor)

                    # Compute the path (for visualization purposes)
                    self.resolution_data["path"] = reconstruct_path(
                        self.resolution_data["cameFrom"], self.resolution_data["current"]
                    )

                    self.resolution_data["total_move_count"] += 1  # We increment the move count

                else:  # No path has been found
                    print("Pas de chemin trouvé.")
                    # We raise a RuntimeError to indicate that no path has been found
                    raise RuntimeError("No path found.")

            elif self.resolution_algorithm == "recursive-backtracking":

                if not self.resolution_data["setupDone"]:
                    self.resolution_data["start_time"] = time.perf_counter()
                    print("Début de la résolution du labyrinthe par backtracking récursif...")
                    self.resolution_data["setupDone"] = True

                if self.resolution_data["stack"][-1] == self.end:  # We have reached the end cell
                    print("Chemin trouvé.")
                    self.resolution_data["is_solved"] = True
                    return True
                else:

                    available = [
                        i
                        for i in self.get_adjacent_cases(self.resolution_data["stack"][-1])
                        if self.can_move(i, self.resolution_data["stack"][-1])
                        and i not in self.resolution_data["banned"]
                        and i not in self.resolution_data["visited"]
                    ]  # We filter the available cells : they must be adjacent, not banned, and not visited

                    if available == []:  # We have reached a dead end : we must backtrack
                        self.resolution_data["banned"].append(self.resolution_data["stack"].pop())

                    else:  # We can still move
                        self.resolution_data["stack"].append(
                            random.choice(available)
                        )  # We choose a random cell to move to
                        self.resolution_data["visited"].append(
                            self.resolution_data["stack"][-1]
                        )  # We mark the cell as visited

                    self.resolution_data["total_move_count"] += 1  # We increment the move count

                    return False
            else:
                print("L'algorithme de résolution n'est pas reconnu.")
                raise NotImplementedError  # We raise a NotImplementedError to indicate that the algorithm is not implemented

    def MD(self, case1, case2):
        """
        Calculates the Manhattan distance between two cells.

        Parameters:
        - case1 (int or tuple): The ID of the first cell or the coordinates of the first cell.
        - case2 (int or tuple): The ID of the second cell or the coordinates of the second cell.

        Returns:
        - int: The Manhattan distance between the two cells.

        """
        if isinstance(case1, int) and isinstance(case2, int):  # Check if the inputs are cell IDs
            case1 = self.id_to_coord(case1)  # Convert the cell ID to coordinates
            case2 = self.id_to_coord(case2)  # Convert the cell ID to coordinates
        return abs(case1[0] - case2[0]) + abs(case1[1] - case2[1])  # Calculate the Manhattan distance

    def resolve_recursive_backtracking(self, start, end):
        """
        Use the recursive backtracking algorithm to find a path from the start cell to the end cell, without storing data for visualization.
        """
        stack = [start]
        banned = []
        visited = []
        while stack[-1] != end:
            available = [
                i
                for i in self.get_adjacent_cases(stack[-1])
                if self.can_move(i, stack[-1]) and i not in banned and i not in visited
            ]
            if available == []:
                banned.append(stack.pop())
            else:
                stack.append(random.choice(available))
                visited.append(stack[-1])
        return stack

    def resolve_a_star(self, start, end):
        """
        Use the A* algorithm to find a path from the start cell to the end cell, without storing data for visualization.
        """

        def h(case):
            return self.MD(case, end)

        def reconstruct_path(cameFrom, current):
            totalPath = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                totalPath.append(current)
            totalPath.reverse()
            return totalPath

        openSet = [start]
        cameFrom = {}

        gScore = {}
        for x in range(self.width * self.height):
            gScore[x] = math.inf
        gScore[start] = 0
        fScore = {}
        for x in range(self.width * self.height):
            fScore[x] = math.inf
        fScore[start] = h(start)

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])
            if current == end:
                path = reconstruct_path(cameFrom, current)
                return path

            openSet.remove(current)
            adjacent = self.get_adjacent_cases(current)
            adjacent = [a for a in adjacent if self.can_move(current, a)]
            for neighbor in adjacent:
                tentative_gScore = gScore[current] + 1
                if tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + h(neighbor)
                    if neighbor not in openSet:
                        openSet.append(neighbor)

        return False

    def get_image(self):

        # Draw the labyrinth

        if not self.has_changed:
            return self.image

        self.image.fill(BUTTON_COLOR)  # We fill the labyrinth with a color

        if DRAW_CASE_NUMBERS:  # We want to draw the case numbers
            for i in range(self.width * self.height):
                coords = self.id_to_coord(i)
                text = font.render(str(i), 0, (255, 255, 255))
                self.image.blit(text, (coords[0] * LABYRINTH_RESOLUTION, coords[1] * LABYRINTH_RESOLUTION))

        for wall in self.walls:
            # Horizontal or vertical wall ?
            orientation = "V" if abs(wall[0] - wall[1]) == 1 else "H"

            case_1_coords = self.id_to_coord(wall[0])

            # If the wall is horizontal :
            if orientation == "H":
                # We want to draw a horizontal line that starts from the bottom-left corner of case 1 to its bottom-right corner.
                # The coordinates of the bottom-left corner are x*LABYRINTH_RESOLUTION, y*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION
                # The coordinates of the bottom-right corner are x*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION, y*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION
                pygame.draw.line(
                    self.image,
                    (255, 255, 255),
                    (
                        case_1_coords[0] * LABYRINTH_RESOLUTION,
                        case_1_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                    ),
                    (
                        case_1_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                        case_1_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                    ),
                    LINE_WIDTH,
                )
            elif orientation == "V":
                pygame.draw.line(
                    self.image,
                    (255, 255, 255),
                    (
                        case_1_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                        case_1_coords[1] * LABYRINTH_RESOLUTION,
                    ),
                    (
                        case_1_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                        case_1_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                    ),
                    LINE_WIDTH,
                )

        self.has_changed = False  # The labyrinth has been drawn, so we don't need to redraw it
        return self.image

    def get_pathfinding_image(self):
        # Draw the pathfinding layer

        if self.generation_data["is_generated"]:

            # Clear the surface
            self.pathfinding_layer.fill((0, 0, 0, 0))

            if self.resolution_algorithm == "recursive-backtracking":

                # We want to draw a line between each cell in the path, and a cross the banned cells.

                path = self.resolution_data["stack"]
                banned = self.resolution_data["banned"]

                for index, case in enumerate(path):
                    if index == 0:  # We don't want to draw a line between the first cell and the cell before it
                        continue
                    case_1_coords = self.id_to_coord(path[index - 1])
                    case_2_coords = self.id_to_coord(case)
                    pygame.draw.line(
                        self.pathfinding_layer,
                        (0, 255, 0),
                        (
                            case_1_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                            case_1_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                        ),
                        (
                            case_2_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                            case_2_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                        ),
                        LINE_WIDTH,
                    )

                for case in banned:  # We want to draw a cross on each banned cell
                    coords = self.id_to_coord(case)
                    top_right = (
                        coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                        coords[1] * LABYRINTH_RESOLUTION,
                    )
                    bottom_left = (
                        coords[0] * LABYRINTH_RESOLUTION,
                        coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                    )

                    pygame.draw.line(self.pathfinding_layer, (255, 0, 0), top_right, bottom_left, LINE_WIDTH)

            elif self.resolution_algorithm == "a-star":

                # We want to draw a line between each cell in the path, and color each cell based on its fScore.

                if self.resolution_data["setupDone"]:  # We only want to draw the path if the setup has been done
                    finite_fScores = [
                        self.resolution_data["fScore"][x]
                        for x in self.resolution_data["fScore"]
                        if self.resolution_data["fScore"][x] != math.inf
                    ]  # We only want to draw the cells with a finite fScore, because the other are pointless and would mess up the color gradient
                    min_fScore = min(
                        finite_fScores
                    )  # We need the minimum and maximum fScores to generate the color gradient
                    max_fScore = max(finite_fScores)

                    for case in range(self.width * self.height):
                        # We don't want to draw the start and end cells, or cells with an infinite fScore
                        if case == self.start or case == self.end or self.resolution_data["fScore"][case] == math.inf:
                            continue
                        coords = self.id_to_coord(case)
                        # Generate a color based on the fScore of the cell
                        color = generate_color(min_fScore, max_fScore, self.resolution_data["fScore"][case])
                        # Draw a colored, semi-transparent rectangle on the cell
                        pygame.draw.rect(
                            self.pathfinding_layer,
                            color + (100,),  # We add an alpha channel to make the color semi-transparent
                            (
                                coords[0] * LABYRINTH_RESOLUTION,
                                coords[1] * LABYRINTH_RESOLUTION,
                                LABYRINTH_RESOLUTION,
                                LABYRINTH_RESOLUTION,
                            ),
                        )

                path = self.resolution_data["path"]  # We get the path from the data

                # This is the same as the recursive backtracking algorithm
                for index, case in enumerate(path):
                    if index == 0:
                        continue
                    case_1_coords = self.id_to_coord(path[index - 1])
                    case_2_coords = self.id_to_coord(case)
                    pygame.draw.line(
                        self.pathfinding_layer,
                        (0, 255, 0),
                        (
                            case_1_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                            case_1_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                        ),
                        (
                            case_2_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                            case_2_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
                        ),
                        LINE_WIDTH,
                    )

        return self.pathfinding_layer
