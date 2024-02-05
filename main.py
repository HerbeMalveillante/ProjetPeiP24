from rich import print
import pygame
import random
import time

from constants import *  # Couleurs, dimensions, etc.
from labyrinth import Labyrinth  # Classe Labyrinth
from graphics import Graphics  # Classe Graphics

# L'objectif de ce fichier main est de faire tourner la boucle principale.
# Afin de maximiser la lisibilité, il est important de faire usage d'un
# maximum de librairies externes.

# Ceci est la seconde version du code, adaptée et transformée pour faciliter
# l'implémentation de futures additions, ainsi que la compréhension de la logique.

# Le programme dispose de plusieurs états :
# -> Le menu qui permet de choisir le mode d'execution (jeu ou automatique)
# ainsi que les paramètres de génération et de résolution du labyrinthe
# -> Le labyrinthe en lui-même, simulé en temps réel ou résolu automatiquement
# -> L'écran de chargement qui s'affiche lors de la génération ou résolution
# (idéalement avec une barre de progression)
# -> Tous les petits écrans intermédiaires qui peuvent être ajoutés par la suite
# Afin de gérer tous ces états, nous allons utiliser un système de pile.
# La pile est une structure de données qui permet de stocker des éléments
# de manière ordonnée. On peut ajouter des éléments au sommet de la pile,
# et on peut en retirer.
# Dans notre cas, la pile va contenir les états du programme. L'état en haut
# de la pile est celui qui est actuellement affiché à l'écran.
# Lorsqu'on veut changer d'état, on ajoute le nouvel état au sommet de la pile,
# et on retire l'ancien état. Ainsi, l'état actuel est toujours au sommet de la pile.
# De cette façon, on peut facilement revenir à l'état précédent en retirant l'état actuel.
# (bouton retour, etc.)

# Dans cette seconde version, nous allons essayer de mettre en place la pile d'états, ainsi qu'un
# mode unique (génération automatique -> Résolution manuelle)


def main():

    L = Labyrinth(30, 30)
    generationTime = L.generate()
    print(f"Generated in {generationTime} seconds")

    G = Graphics()

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        G.draw(L)

    # Quit the game
    pygame.quit()


main()
