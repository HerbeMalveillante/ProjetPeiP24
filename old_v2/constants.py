# Ce fichier contient les constantes, valeurs par défaut et paramètres utilisés dans le programme.
# Il est possible de modifier ces valeurs manuellement pour changer le comportement du programme.
# Ces valeurs ne seront jamais modifiée par le programme lui-même, mais éventuellement écrasées par
# des paramètres internes.

# COULEURS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GRAY = GREY

# GUI
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
WINDOW_TITLE = "Labyrinthe"

# PARAMETRES PAR DEFAUT
DRAW_CASE_NUMBERS = False  # Si True, les cases afficheront leur numéro unique.
SHOW_FPS = True
PIXEL_PERFECT = False  # Si True, les cases auront une taille entière. Cela affichera le labyrinthe légèrement plus petit que la taille maximale si ses dimensions ne sont pas des multiples de la taille maximale.
FPS_RESOLUTION = 2  # En secondes : on calcule le FPS en mesurant la moyenne du nombre de frames par seconde sur cette durée. Plus cette valeur est grande, plus le FPS est stable, mais moins il est précis.
ANTIALIASING = 1  # 0: désactivé, 1: activé
