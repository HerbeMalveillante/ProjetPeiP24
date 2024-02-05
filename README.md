# Projet Peip2 2023-2024 : Labyrinthe

## Modifications apportées le 05/02/2024
- Réorganisation du code dans des fichiers qui font plus de sens
- Ajout d'un fichier dans lesquelles sont stockées les constantes, valeurs par défaut et paramètres du programme
- Ajout d'un compteur de FPS
- Correction du bug qui empêchait la génération de labyrinthes non carrés
- Nouvelle structure des graphiques sous forme de classe qui permettra de rajouter plus facilement des fonctionnalités.
- Les anciennes versions des fichiers ont été stockées dans un dossier "old" pour le moment mais pourront être supprimées par la suite : GitHub garde une trace dans tous les cas

### Ce qu'il reste à implémenter pour retrouver toutes les fonctionnalités avant le refactoring :
- Menu principal permettant de lancer la génération d'un labyrinthe
- Personnage qui peut se déplacer dans le labyrinthe et le résoudre (attention à résoudre les bugs qui permettent de se téléporter d'un bout à l'autre du labyrinthe)
- Personnage qui peut terminer la résolution du labyrinthe en atteignant la fin, et est chronométré
- Écran de chargement affiché pendant la génération du labyrinthe, avec une barre de progression ce serait super

## TODOLIST à faire ensemble : 
- Implémenter un algorithme de résolution basique
- Ajouter la possibilité de faire résoudre le labyrinthe par l'algorithme dans le menu
- Possibilité de customiser la taille du labyrinthe avant la génération
- Possibilité de customiser le loopingfactor avant la génération
