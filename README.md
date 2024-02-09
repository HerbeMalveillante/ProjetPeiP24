# Projet Peip2 2023-2024 : Labyrinthe

## Modifications 09/02/24

- Résolution d'un bug qui affichait par défaut l'animation de résolution du labyrinthe dans le mode "play" (résolution manuelle)
- Première optimisation de la résolution automatique : FPS stable sur des labyrinthes de taille moyenne
- Ajout d'un fichier launch.json qui permet de lancer le programme depuis n'importe quel fichier avec VSCode

### Problèmes de performance dans le mode "résolution animée"

Les FPS chutent drastiquement quand on utilise le mode "résolution animée". Dans les faits, c'est compréhensible car on ajoute les indicateurs de cases bannies et visitées de façon dynamique, et elles sont donc modifiées à chaque frame, rendant l'utilisation du cache impossible.

Quelques pistes à envisager :

- Séparer le cache du labyrinthe et le cache de l'interface de résolution (ligne de chemin, cases visitées, cases bannies, etc.) : Ainsi, on peut charger le cache du labyrinthe et simplement dessiner les lignes de résolution par dessus. Ça implique par contre de faire un gros refactoring sur la structure de données du cache et/ou des données de labyrinthe. En effet, les données de résolution sont actuellement stockées directement dans l'objet labyrinthe.
- On pourrait également modifier le cache pour ne pas tenir compte des modifications apportées aux données de résolution, et les charger/afficher séparément
- Éventuellement du multithreading ? Ça serait beaucoup plus compliqué mais c'est toujours faisable

- Optimiser l'affichage des cases bannies / visitées : On dessine pour l'instant de multiples lignes diagonales alors qu'on pourrait dans la plupart des cas en dessiner une seule. Toutefois, le problème subsistera toujours sur des labyrinthes de grande taille.
- L'avantage de cette seconde solution est qu'elle peut être implémentée de façon concurrente à la solution précédente : je vais commencer par l'ajouter et je me concentrerai sur la mise à jour de la logique du cache par la suite.
- Cette modification peut également être apportée à la fonction qui dessine le labyrinthe dans un premier temps, ce qui permettra d'animer la génération du labyrinthe en utilisant différents algorithmes. A garder en tête.
