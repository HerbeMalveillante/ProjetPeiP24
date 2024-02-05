import pygame
import graph2
import time

pygame.init()
screen_width = 1280
screen_height = 800
font = pygame.font.Font("freesansbold.ttf", 20)
graph2.init(sw=screen_width, sh=screen_height, fnt=font)
pygame.display.set_caption("Labyrinth")
screen = pygame.display.set_mode((screen_width, screen_height))
L = graph2.Labyrinth(25, 25, 30)
C = graph2.Character(labyrinth=L)


STATE = "MENU"


class Colors(object):
    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


class Menu(object):
    def __init__(self):
        self.buttons = []

    def draw(self):
        # Draw the menu
        # fill the screen
        screen.fill(Colors.WHITE)
        for button in self.buttons:
            button.draw()

    def addButton(self, button):
        self.buttons.append(button)


class LoadingScreen(object):
    def __init__(self):
        pass

    def draw(self):
        # Draw the menu
        # fill the screen
        screen.fill(Colors.WHITE)
        # write "loading"
        text = font.render("Loading", True, Colors.BLACK)
        textRect = text.get_rect()
        textRect.center = (screen_width / 2, screen_height / 2)
        screen.blit(text, textRect)


class Button(object):
    def __init__(
        self,
        topLeft,
        width,
        height,
        color=Colors.GREY,
        text="Hello World",
        on_click=None,
    ):
        self.topLeft = topLeft
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.on_click = on_click

    def draw(self):
        pygame.draw.rect(
            screen, self.color, pygame.Rect(self.topLeft, (self.width, self.height))
        )
        text = font.render(self.text, True, Colors.BLACK)
        textRect = text.get_rect()
        textRect.center = (
            self.topLeft[0] + self.width / 2,
            self.topLeft[1] + self.height / 2,
        )
        screen.blit(text, textRect)


class Timer(object):
    def __init__(self, duration):
        self.duration = duration
        self.elapsed = 0
        self.state = "STOPPED"

    def start(self):
        self.state = "RUNNING"

    def reset(self):
        self.elapsed = 0
        self.state = "STOPPED"

    def addTimeElapsed(self, timeElapsed):
        if self.state == "RUNNING":
            self.elapsed += timeElapsed

    def hasRang(self):
        return self.elapsed >= self.duration


def changeState(state):
    global STATE
    STATE = "LOADING"
    L.generate()
    STATE = state


LS = LoadingScreen()
M = Menu()
M.addButton(
    Button(
        (100, 100),
        300,
        100,
        on_click=lambda: changeState("GAME"),
    )
)
TMessageEnd = Timer(5)

# Game loop
running = True
last_frame = time.time()
while running:
    if STATE == "GAME":
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                key = pygame.key.name(event.key)
                if key == "up":
                    C.move("U")
                elif key == "down":
                    C.move("D")
                elif key == "left":
                    C.move("L")
                elif key == "right":
                    C.move("R")

                print(
                    f"""Key Pressed : {pygame.key.name(event.key)}
    position : {C.caseId}"""
                )

        # Simulation

        # Le joueur apparaît sur la carte
        # On lui indique qu'il doit résoudre le labyrinthe en étant chronométré
        # Il doit ensuite se déplacer et atteindre la sortie
        # Quand il atteint la sortie, on lui indique le temps réalisé, les mouvements effectués
        # On on le renvoie à l'accueuil.

        if C.caseId == L.end:
            TMessageEnd.start()
            # print(TMessageEnd.elapsed)
            TMessageEnd.addTimeElapsed(time.time() - last_frame)
            if TMessageEnd.hasRang():
                TMessageEnd.reset()
                STATE = "MENU"

        # Drawing

        if C.moveCount > 0:
            L.addTimeElapsed(time.time() - last_frame)
        last_frame = time.time()

        L.draw(screen)
        C.draw(screen)
        if TMessageEnd.state == "RUNNING":
            text = font.render("Bravo !", True, Colors.BLACK)
            textRect = text.get_rect()
            textRect.center = (screen_width / 2, screen_height / 2)
            screen.blit(text, textRect)

        pygame.display.flip()  # Update the display

    elif STATE == "MENU":
        # Event handling

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for button in M.buttons:
                    if (
                        pos[0] > button.topLeft[0]
                        and pos[0] < button.topLeft[0] + button.width
                        and pos[1] > button.topLeft[1]
                        and pos[1] < button.topLeft[1] + button.height
                    ):
                        if button.on_click is not None:
                            LS.draw()
                            pygame.display.flip()
                            button.on_click()
                            break

        M.draw()

        pygame.display.flip()  # Update the display
    elif STATE == "LOADING":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        LS.draw()
        pygame.display.flip()


# Quit the game
pygame.quit()
