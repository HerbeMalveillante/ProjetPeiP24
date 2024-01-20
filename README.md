Bon alors je suis en train de réfléchir à la meilleure structure de données pour représenter notre labyrinthe.

Imaginons que notre labyrinthe soit un graphe. 

On a un certain nombre de cases, et il est possible de se déplacer de case en case pourvu qu'une connexion existe entre elles. Si aucune connexion n'existe, cela signifie que les cases ne sont pas adjacentes, ou qu'elles sont séparées par un mur.

Le souci, c'est que l'absence de connexion ne signifie pas forcément qu'il y a un mur : les deux cases peuvent simplement ne pas être adjacentes.

Pour la génération du labyrinthe, on utilise souvent un algorithme de type "recursive backtracker". Cet algorithme consiste à choisir une case au hasard, puis à choisir une case adjacente à cette case au hasard, et à répéter l'opération jusqu'à ce qu'on ne puisse plus choisir de case adjacente. On revient alors en arrière jusqu'à ce qu'on puisse choisir une case adjacente à la case précédente, et on répète l'opération jusqu'à ce qu'on ait visité toutes les cases.

Il faut donc qu'on puisse facilement choisir une case adjacente à une case donnée. 
Imaginons qu'on aie une matrice qui représente toutes les cases du labyrinthe, permettant de facilement trouver une case à partir de ses coordonnées et donc les cases adjacentes.

On va ensuite avoir une liste de murs. Chaque mur est représenté par deux cases adjacentes. Si un tuple de deux cases adjacentes est dans la liste, alors il y a un mur entre ces deux cases.