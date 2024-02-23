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

# Partie créative

Qu'est-ce qu'on a :

- Un labyrinthe
- Un personnage
- Un moyen de faire des labyrinthes à l'infini
- Un moyen de résoudre les labyrinthes
- Eventuellement la caméra qui bouge pour ajouter un côté "jeu"

Qu'est-ce qu'on pourrait faire :

- Jeu ? Améliorer les algos / leur mettre des bâtons dans les roues ?
- Téléporteurs
- Murs qui bougent
- Plusieurs étages (escaliers, trous qui permettent juste de descendre)

- Jeu : chronométré / en mode "roguelite"

## Premier jet

- Mélange "pac man" / "roguelite"
- Le joueur doit récupérer des points disséminés dans le labyrinthe.
- Les points sont générés aléatoirement de différentes façons (coffres, etc)
- Le labyrinthe a des trucs qui permettent de naviguer différamment (téléporteurs, etc)
- Des ennemis se déplacent avec des algorithmes différents (random, main droite, a\*, etc)
- Le joueur peut se déplacer, et éventuellement trouver des bonus comme par exemple pouvoir poser des murs que seul lui peut franchir
- Le joueur peut se rendre à la fin du niveau quand il le souhaite pour valider ses points.
- Le joueur avec le plus de points est sacré champion de la salle de TP.

- Plusieurs niveaux de difficulté en fonction du looping factor du labyrinthe (les IA sont fortes pour trouver des chemins dedans, un humain l'est beaucoup moins)


