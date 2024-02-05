# Librairie pour améliorer la lisibilité des matrices et autres structures de données dans le terminal.
# Elle n'est pas nécessaire pour le fonctionnement du programme et peut être retirée sans problème.
from rich import print

# Librairies externes nécéssaies pour le fonctionnement du programme
import pygame
import random
import time

# Import des classes et fonctions du programme
from constants import *  # Couleurs, dimensions, etc.
from labyrinth import Labyrinth  # Classe Labyrinth
from graphics import Graphics  # Classe Graphics
from menu import *  # Classe Menu

# L'objectif de ce fichier main est de faire tourner la boucle principale.
# Afin de maximiser la lisibilité, il est important de faire usage d'un
# maximum de librairies externes.

# Ceci est la seconde version du code, adaptée et transformée pour faciliter
# l'implémentation de futures additions, ainsi que la compréhension de la logique.


def main():

    L = Labyrinth(30, 30)  # Création d'un labyrinthe de 30x30 cases
    L2 = Labyrinth(20, 20)  # Création d'un second labyrinthe de 20x20 cases
    generationTime = L.generate()  # Génération du labyrinthe
    print(f"Generated in {generationTime} seconds")
    generationTime2 = L2.generate()  # Génération du second labyrinthe
    print(f"Generated in {generationTime2} seconds")

    G = Graphics()  # Initialisation de la classe Graphics

    # Boucle principale
    running = True
    while running:
        # On vérifie les événements : par exemple la fermeture de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        G.clearScreen()  # Efface l'écran
        G.drawLabyrinth(L, pos=(10, 10), size=(400, 400))  # Dessin du labyrinthe 1
        G.drawLabyrinth(L2, pos=(420, 10), size=(400, 400))  # Dessin du labyrinthe 2
        G.flip()  # Affiche l'écran (évite les clignotements en dessinant plusieurs objets à la suite)

    # Quit the game
    pygame.quit()


menu = Menu()
menu.main()
