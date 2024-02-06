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


menu = Menu()
menu.main()
