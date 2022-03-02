 
 # Programme de gestion de tournoi d'échecs (règle suisse).
 
[Repo github P4_devant_xavier](https://github.com/XDevant/P4_devant_xavier)

### Usage:

Pour taper une commande, il faut taper '.' suivi des initiales de la commandes, séparer la commande des valeurs par un espace et les valeurs par des virgules

**Exemple:**

 .nj Lambert, Alphonse, 22/06/1970, genre=M
 
 Si les valeurs sont incorrectes ou si vous tapez juste la commande, vous serez orienté vers un sous menu qui précisera les valeurs manquantes et leur nom (clef).
 Il n'est pas neccessaire de taper la commande depuis un sous menu, les valeurs suffisent.
 Pour changer une valeur déjà entrée, il faut la donner sous la forme de clef=valeur comme pour genre dans l'exemple.


### Liste des commandes:

    Nouveau Joueur : .nj nom,prénom, date_de_naissance, genre, rang='auto'
Le rang d'un nouveau joueur est attribué de façon automatique lors de sa création et égal au nombre d'inscrits. 

    Nouveau Tournoi: .nt nom, lieu, date, description, règle, rondes=4
Le nombre de rondes est attribué à 4 par défault
    règles possibles : blitz, coup rapide, bullet

    Modifier Joueur: .mj joueur, classement
Modifie le classement d'un joueur. 
 Ex: .mj 1, 7  Le joueur dont l'identifiant est 1 est maintenant 7eme au classement.

    Modifier Tournoi: .mt tournoi, joueur
Permet d'inscrire un joueur dans un tournoi. Ou de le désinscrire s'il est déjà inscrit. Une confirmation sera alors demandée

    Modifier Round: .mr tournoi, joueur, score
Permet de renseigner le score d'un joueur pour le round en cours. Le score de l'autre joueur est attribué automatiquement s'il est encore vide
 scores possibles: 1, 0, 0.5, ou V, N, D

    Démarrer Tournoi: .dt tournoi
Démarre un tournoi si le nombre d'inscrits est strictement supérieur au nombre de rondes et pair. Une confirmation sera demandée.

    Démarrer Ronde: .dr ou .dt tournoi
Démarre une nouvelle ronde si la précédente est terminée.

    Clore Tournoi: .ct ou .dt tournoi
Clos un tournoi si la dernière ronde est terminée.

    Sauver: .s
Sauve l'état du programme (tournois et joueurs en cours de création, menu) et quitte. Les joueurs, tournois, rondes et matchs sont sauvés automatiqument à chaque modification. Une confirmation sera demandée.

    Quitter: .q
Permet de quitter sans sauver. Une confirmation sera demandée.

    Réinitialiser: .r
Remet à zéro l'état du programme. Equivalent à sauver sans quitter.

    Liste des Joueurs: .lj
Affiche la liste des joueurs inscrits par ordre alphabétique.

    Liste des Classements: .lc
Affiche la liste des joueurs en fonction de leur classement.

    Liste des Tournois: .lt
Affiche la liste des tournois.
    
    Liste des Joueurs en Tournoi: .ltj tournoi
Affiche la liste des joueurs inscrits au tournoi par ordre alphabétique.

    Liste des Classements en Tournoi: .ltc tournoi
Affiche la liste des joueurs inscrits au tournoi en fonction de leur classement.

    Liste des Rounds du Tournoi: .ltr tournoi
Affiche la liste des rondes du tournoi.

    Liste des matches du Tournoi: .ltm
Affiche la liste des matchs du tournoi.

    Liste des Scores des Joueurs du Tournoi: .lts
Affiche la liste des joueurs inscrits au tournoi en fonction de leur score dans le tournoi

    Liste des Actions: .la
Affiche la liste des actions (commandes)
    
    
 ### Menus:
 
 Si une commande est entrée sans les valeurs nécessaires, elle affichera un sous menu expliquant ce qu'elle a compris comme valeur et celles qui lui manquent.
 
Exemple

    Entrez une commande: .nj joe cabbot

 Valeurs fournies insuffisantes pour la commande: Nouveau Joueur
 
 Valeurs actuelles:  {'nom': 'joe cabbot', 'prénom': '?', 'date de naissance': '?', 'genre': '?', 'classement': 'auto'}

    Entrez prénom, date de naissance, genre: nom=cabbot, prénom=joe, 22/11/1967,M

 Nouveau Joueur crée:
(13)joe cabbot classement: 13

    Entrez une commande:

### Tournoi par défaut:

 Lorsqu'un tournoi est crée ou modifié, il devient le tournoi par défaut.
 Lorsqu(un tournoi est démarr ou ses résultats modifiés (commandes mr, dt, dr) il devient le tournoi actif par défaut.
 
  La valeur par defaut est attribuée d'office à la commande.
  Pour gérer plusieurs tournois, il faut soit:
  
  1. reset les valeurs par defaut avant de changer de tournoi
   
  2. entrer l'id du nouveau tournoi à gérer avec sa clef (tournoi=5)
   
   

