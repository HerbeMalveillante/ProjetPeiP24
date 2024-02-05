TODO : Régler le problème de génération du labyrinthe quand n!=m



Idées pour la partie "perso"

- Rajouter des éléments qui changent la structure du labyrinthe : murs qui bouges, téléporteurs, colonnes qui se déplacent, etc.
- Permet d'adapter les algos de résolution avec nos contraintes perso
- Chronométrer la résolution



Écran-titre : sélection des options PUIS lancer la simulation

Un mode "jeu" -> le joueur doit résoudre le laby
    -> "Mode classique" (avec les labys plus ou moins durs ?)
    -> "Mode custom" (on bidouille comme on veut)
Un mode "IA" -> On choisit une ia et on tweake le laby et on le résoud
    -> Comparaisons IA / Benchmark


1 fichier "graphique" (fonctions pygame) (peut être)
1 fichier "logique du labyrinthe"
1 fichier main qui gère la boucle d'execution



2 Bugs découverts le 02/02/23 : 
- On peut warp d'un côté à l'autre de la map par défaut (modifier fonction move)
- On Relancer une partie après un retour au menu ne reset ni le labyrinthe ni le personnage

A FIXER





Reformatting : 

-> Séparer fonctions graphiques et fonctions logiques
-> Logique du labyrinthe dans un seul fichier
-> Un fichier "graphique" avec une fonction "draw" qui va dessiner la fenêtre et tout
-> Améliorer la state machine ?
-> Optimisations
-> Résoudre les bugs pointés ce weekend
-> En gros tout remettre dans des fichiers différents