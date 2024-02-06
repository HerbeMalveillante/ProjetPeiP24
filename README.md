# Projet Peip2 2023-2024 : Labyrinthe

## Modifications apportées le 05/02/2024
- Réorganisation du code dans des fichiers qui font plus de sens
- Ajout d'un fichier dans lesquelles sont stockées les constantes, valeurs par défaut et paramètres du programme
- Ajout d'un compteur de FPS
- Correction du bug qui empêchait la génération de labyrinthes non carrés
- Nouvelle structure des graphiques sous forme de classe qui permettra de rajouter plus facilement des fonctionnalités.
- Les anciennes versions des fichiers ont été stockées dans un dossier "old" pour le moment mais pourront être supprimées par la suite : GitHub garde une trace dans tous les cas
- Possibilité de dessiner un labyrinthe à n'importe quelle taille et à n'importe quel emplacement de l'écran, permettant de faciliter l'implémentation du menu ou d'afficher plusieurs labyrinthes à la fois.
- Ajout de TOUT le système de Menu qui pète sa mère et est super vraiment trop bien.

## Modifications apportées le 06/02/2024
- Ajout du système de cache permettant d'avoir une performance optimale même en dessinant d'énormes labyrinthes.
- Mise à jour du code permettant de modifier la taille et la position du labyrinthe de façon à fonctionner avec le cache.
- Personnage PARTIELLEMENT implémenté : encore des bugs dans la navigation

## TODOLIST
- Personnage qui peut se déplacer dans le labyrinthe et le résoudre
- Personnage qui peut terminer la résolution du labyrinthe en atteignant la fin, et est chronométré
- Écran de chargement affiché pendant la génération du labyrinthe, avec une barre de progression ce serait super
- Implémenter un algorithme de résolution basique
- Ajouter la possibilité de faire résoudre le labyrinthe par l'algorithme dans le menu
- Possibilité de customiser la taille du labyrinthe avant la génération
- Possibilité de customiser le loopingfactor avant la génération



## A propos du cache du labyrinthe :

Dessiner tout le labyrinthe à partir de primitifs à chaque frame est coûteux en ressources, et il est possible de gagner en performance en dessinant le labyrinthe une seule fois dans une texture, et en dessinant cette texture à chaque frame. Cela permettrait également de ne pas avoir à recalculer le labyrinthe à chaque frame, ce qui est un avantage non négligeable.

La texture serait créée à la génération du labyrinthe, et serait ensuite dessinée à chaque frame. Si le labyrinthe est modifié, la texture est recalculée.




