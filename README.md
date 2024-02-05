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

### Ce qu'il reste à implémenter pour retrouver toutes les fonctionnalités avant le refactoring :
- Menu principal permettant de lancer la génération d'un labyrinthe
- Personnage qui peut se déplacer dans le labyrinthe et le résoudre (attention à résoudre les bugs qui permettent de se téléporter d'un bout à l'autre du labyrinthe)
- Personnage qui peut terminer la résolution du labyrinthe en atteignant la fin, et est chronométré
- Écran de chargement affiché pendant la génération du labyrinthe, avec une barre de progression ce serait super

### Implémentation du menu avec la structure actuelle :

On a pour l'instant un code très propre divisé en plusieurs classes, ici graphiques et logiques.
Les fonctions qui permettent de faire fonctionner le menu sont un mélange des deux, et auront du mal à entrer dans une seule de ces catégories.
Dans ces conditions, la meilleure façon de faire serait de créer une nouvelle classe qui gère le menu. Cette classe pourrait être appelée par la classe principale, et pourrait appeler les fonctions de la classe logique pour générer un labyrinthe, par exemple, ou les fonctions de la classe graphique pour afficher le labyrinthe et les boutons du menu.



## TODOLIST à faire ensemble : 
- Implémenter un algorithme de résolution basique
- Ajouter la possibilité de faire résoudre le labyrinthe par l'algorithme dans le menu
- Possibilité de customiser la taille du labyrinthe avant la génération
- Possibilité de customiser le loopingfactor avant la 
- Taille du FRAME_BUFFER qui s'adapte en temps réel au FPS. En effet, si le FPS est très haut, le FPS affiché change constamment, ce qui est très désagréable. Il faudrait que le FRAME_BUFFER s'adapte à la taille du FPS pour que le FPS bouge moins et soit représentatif de la dernière seconde par exemple.





