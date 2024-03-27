import pygame
import time
import random
from constants import LABYRINTH_RESOLUTION, DRAW_CASE_NUMBERS, BUTTON_COLOR, LINE_WIDTH, font
import math


class Labyrinth(pygame.sprite.Sprite):

    def __init__(self, parent, size, generation_algorithm, resolution_algorithm, looping_factor):
        super().__init__()

        self.parent = parent
        self.width = size[0]
        self.height = size[1]
        self.matrix = [[j + i * self.width for j in range(self.width)] for i in range(self.height)]

        self.image = pygame.Surface((self.width * LABYRINTH_RESOLUTION, self.height * LABYRINTH_RESOLUTION))
        self.pathfinding_layer = pygame.Surface(
            (self.width * LABYRINTH_RESOLUTION, self.height * LABYRINTH_RESOLUTION), pygame.SRCALPHA, 32
        )
        self.rect = self.image.get_rect()
        self.has_changed = True

        self.walls = []

        self.start = 0
        self.end = self.width * self.height - 1

        self.generation_algorithm = generation_algorithm
        self.resolution_algorithm = resolution_algorithm

        self.looping_factor = looping_factor

        current = random.randint(0, self.width * self.height - 1)
        self.generation_data = {
            "is_generated": False,
            "generation_time": 0,
            "step": 0,
            "stack": [current],
            "visited": [current],
            "wall_index": 0,
            "perfect_wall_count": 0,
        }

        self.resolution_data = {
            "is_solved": False,
            "resolution_time": 0,
            "stack": [self.start],
            "banned": [],
            "visited": [],
            "total_move_count": 0,
        }

        self.vertical_wall_surface = pygame.Surface((2, LABYRINTH_RESOLUTION))
        self.vertical_wall_surface.fill((0, 0, 0))
        self.horizontal_wall_surface = pygame.Surface((LABYRINTH_RESOLUTION, 2))
        self.horizontal_wall_surface.fill((0, 0, 0))

    def id_to_coord(self, id):
        return (id % self.width, id // self.width)

    def coord_to_id(self, x, y=None):
        if y is None:
            y = x[1]
            x = x[0]
        return y * self.width + x

    def is_adjacent(self, case_1, case_2):
        case_1, case_2 = min(case_1, case_2), max(case_1, case_2)
        return case_1 in self.get_adjacent_cases(case_2)

    def get_adjacent_cases(self, case):

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
        if not self.is_adjacent(case_1, case_2):
            print(f"Impossible d'ajouter un mur : les cases {case_1} et {case_2} ne sont pas adjacentes.")
            return False
        case_1, case_2 = min(case_1, case_2), max(case_1, case_2)
        if (case_1, case_2) not in self.walls:
            self.walls.append((case_1, case_2))
            self.has_changed = True
            return True
        return False

    def remove_wall(self, case_1, case_2):
        case_1, case_2 = min(case_1, case_2), max(case_1, case_2)
        if (case_1, case_2) in self.walls:
            self.walls.remove((case_1, case_2))
            self.has_changed = True
            return True
        print(f"Il n'y a pas de mur entre les cases {case_1} et {case_2}.")
        return False

    def fill_with_walls(self):
        for i in range(self.width * self.height):
            if i >= self.width * self.height - 1:
                continue
            localIterator = i % self.width
            # Horizontal
            if (i + 1) % self.width > localIterator:
                self.add_wall(i, i + 1)
            # Vertical
            if i + self.width < self.width * self.height:
                self.add_wall(i, i + self.width)

    def can_move(self, case_1, case_2):
        case1, case2 = min(case_1, case_2), max(case_1, case_2)
        if not self.is_adjacent(case1, case2):
            return False
        if (case1, case2) in self.walls:
            return False
        return True

    def generate_step(self):

        start_time = time.perf_counter()

        if not self.generation_data["is_generated"]:

            if self.generation_algorithm == "dead-end-filling":
                if self.generation_data["step"] == 0:  # Wall filling
                    self.fill_with_walls()
                    self.generation_data["step"] = 1
                    print("Première étape terminée : remplissage des murs.")
                    return False
                elif self.generation_data["step"] == 1:  # Dead-end filling

                    if len(self.generation_data["stack"]) == 0:
                        self.generation_data["step"] = 2
                        self.generation_data["perfect_wall_count"] = len(self.walls)
                        print("Deuxième étape terminée : labyrinthe parfait généré.")
                        return False

                    else:
                        current = self.generation_data["stack"][-1]
                        adjacent_cases = self.get_adjacent_cases(current)
                        unvisited_adjacent_cases = [
                            case for case in adjacent_cases if case not in self.generation_data["visited"]
                        ]

                        if len(unvisited_adjacent_cases) == 0:
                            self.generation_data["stack"].pop()
                            return False

                        next_case = random.choice(unvisited_adjacent_cases)
                        self.remove_wall(current, next_case)
                        self.generation_data["visited"].append(next_case)
                        self.generation_data["stack"].append(next_case)

                    # print(f"{len(self.walls)} murs restants.")

                elif self.generation_data["step"] == 2:  # looping factor

                    # On veut supprimer 10% des murs, donc on en chope 10% au hasard et on les supprime

                    if self.looping_factor != 0:
                        for _ in range(int(len(self.walls) * self.looping_factor)):
                            wall = random.choice(self.walls)
                            self.remove_wall(wall[0], wall[1])
                    self.generation_data["is_generated"] = True
                    self.generation_data["step"] = 3
                    print("Troisième et dernière étape terminée : murs aléatoires supprimés.")
                    self.generation_data["is_generated"] = True
                    self.generation_data["step"] = 3
                    return True

            else:
                print("L'algorithme de génération n'est pas reconnu.")
                exit(1)

        end_time = time.perf_counter()
        self.generation_data["generation_time"] += end_time - start_time

    def resolve_step(self):

        start_time = time.perf_counter()
        if not self.resolution_data["is_solved"]:

            if self.resolution_algorithm == "a-star":
                pass
            elif self.resolution_algorithm == "recursive-backtracking":
                if self.resolution_data["stack"][-1] == self.end:
                    self.resolution_data["is_solved"] = True
                    return True
                else:
                    available = [
                        i
                        for i in self.get_adjacent_cases(self.resolution_data["stack"][-1])
                        if self.can_move(i, self.resolution_data["stack"][-1])
                        and i not in self.resolution_data["banned"]
                        and i not in self.resolution_data["visited"]
                    ]

                    if available == []:
                        self.resolution_data["banned"].append(self.resolution_data["stack"].pop())

                    else:
                        self.resolution_data["stack"].append(random.choice(available))
                        self.resolution_data["visited"].append(self.resolution_data["stack"][-1])

                    self.resolution_data["total_move_count"] += 1

                    return False
            else:
                print("L'algorithme de résolution n'est pas reconnu.")
                exit(1)

    def MD(self, case1, case2):
        if isinstance(case1, int) and isinstance(case2, int):
            case1 = self.id_to_coord(case1)
            case2 = self.id_to_coord(case2)
        return abs(case1[0] - case2[0]) + abs(case1[1] - case2[1])

    def resolve_recursive_backtracking(self, start, end):
        """
        Retourne une liste de positions qui mène de la case de départ à la case d'arrivée, sans stocker de données pour visualisation
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
                # stack.append(available[-1])
                visited.append(stack[-1])
        return stack

    def resolve_a_star(self, start, end):
        """
        Retourne une liste de positions qui mène de la case de départ à la case d'arrivée, sans stocker de données pour visualisation
        Utilise l'algorithme A* pour trouver le chemin le plus court
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

        if not self.has_changed:
            return self.image

        self.image.fill(BUTTON_COLOR)

        # blit_sequence = []

        if DRAW_CASE_NUMBERS:
            # On veut dessiner le numéro de case sur chaque case
            for i in range(self.width * self.height):
                coords = self.id_to_coord(i)
                text = font.render(str(i), 0, (255, 255, 255))
                self.image.blit(text, (coords[0] * LABYRINTH_RESOLUTION, coords[1] * LABYRINTH_RESOLUTION))

        # On dessine un rond pour la case actuelle dans la génération
        # if not self.generation_data["is_generated"]:
        #     current_coords = self.id_to_coord(self.generation_data["stack"][-1])
        #     pygame.draw.circle(
        #         self.image,
        #         (255, 255, 255),
        #         (
        #             current_coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
        #             current_coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION // 2,
        #         ),
        #         LABYRINTH_RESOLUTION // 4,
        #     )

        for wall in self.walls:
            # Horizontal or Vertical ?
            orientation = "V" if abs(wall[0] - wall[1]) == 1 else "H"

            case_1_coords = self.id_to_coord(wall[0])

            # Si le mur est horizontal :
            if orientation == "H":
                # On veut dessiner une ligne horizontale qui commence du coin inférieur gauche de la case 1 jusqu'à son coin inférieur droit.
                # Les coordonnées du coin inférieur gauche c'est x*LABYRINTH_RESOLUTION, y*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION
                # Les coordonnées du coin inférieur droit c'est x*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION, y*LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION
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

        # self.image.fblits(blit_sequence)
        self.has_changed = False
        return self.image

    def get_pathfinding_image(self):
        # Opti : on sépare le pathfinding de l'affichage du labyrinthe : il ne change plus donc pas besoin de
        # le recalculer à chaque frame, autant mettre ça sur un layer différent on est plus à un blit près...

        if not self.resolution_data["is_solved"] and self.generation_data["is_generated"]:
            # On veut dessiner une ligne qui part de la case de départ et qui suit le chemin jusqu'à la dernière case de la stack
            # Et on veut barrer les cases bannies

            # Clear the surface
            self.pathfinding_layer.fill((0, 0, 0, 0))

            path = self.resolution_data["stack"]
            banned = self.resolution_data["banned"]

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

            for case in banned:
                coords = self.id_to_coord(case)
                top_right = (coords[0] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION, coords[1] * LABYRINTH_RESOLUTION)
                bottom_left = (
                    coords[0] * LABYRINTH_RESOLUTION,
                    coords[1] * LABYRINTH_RESOLUTION + LABYRINTH_RESOLUTION,
                )

                pygame.draw.line(self.pathfinding_layer, (255, 0, 0), top_right, bottom_left, LINE_WIDTH)

        return self.pathfinding_layer
