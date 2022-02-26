class Help:
    def __init__(self):
        self.intro = ["Ce programme permet principalement de faire les 3 choses suivantes:",
                      "Enregistrer une nouveau joueur dans la base de données par exemple en tapant '.nj' et en suivant le guide.",
                      "Enregistrer une nouveau tournoi dans la base de données '.nt' et suivre les instructions.",
                      "Gérer un tournoi '.mt' permet d'inscrire des joueurs dans le tournoi, '.dt' de le démarrer",
                      "Ensuite, '.mr' permet de gérer les rondes du tournoi",
                      "",
                      "Une action utilisateur commence par un '.' suivi de 1 à 3 lettres. Par ex: .lt affiche le liste des tournois",
                      "cette action peut être suivie d'un espace et de plusieurs valeurs séparées par des ','.",
                      "Par ex: '.mj 15, age=51' change l'age du joueur dont l'id est 15",
                      "Cependant si vous tapez simplement '.ja' le programme vous expliquera comment Actualiser un Joueur."
                      "",
                      "'.a' se combine avec toute commande et affiche l'aide de la commande.('.adt' affiche l'aide de '.dt')",
                      "",
                      "Conseil n°1: essayez les commandes, toute interaction avec la base de donnée demande une confirmation",
                      "Conseil n°2: terminez les créations de tournois ou de nouveau joueurs que vous commencez pour limiter les messages"
                     ]
        self.base = ["Enter fait défiler l'aide '.' permet de sortir de l'aide",
                     "Tapez '.aa' pour la liste des actions simples et des menus des actions complexes",
                     "Tapez '.aj' / '.at' / '.ar' pour la liste des actions complexes sur les Joueurs/Tournois ou Rondes",
                     "Tapez '.a' suivi du nom d'une commande pour afficher l'aider liée à la commande",
                     "Conseil n°1: essayez les commandes, toute interaction avec la base de donnée demande une confirmation",
                     "Conseil n°2: terminez les créations de tournois ou de nouveau joueurs que vous commencez pour limiter les messages"
                    ]
        self.injonctions = ["(.Q)uitter : (.q, .x) propose de quitter en sauvant ou sans sauver.",
                            "(.S)auver : (.s, .w) sauve les items en cours de création, les valeurs par défaut et le menu en cours",
                            "(.A)ide : (.a, .h) affiche l'aide",
                            "(..) : remonte l'arbre des menus",
                            "(.R) : réinitialise les valeurs en cours de saisie",
                            "(.O) : affiche les options et permet de les modifier"
                           ]
        self.commands = ["(.N)ouveau (J)oueur (nom, prénom, date de naissance, genre, classement): crée un nouveau joueur"
                         "(.M)odifier (J)oueur (joueur_id, classement): actualise un joueur, son classement par défaut",
                         "(.N)ouveau (T)ournoi (nom, place, date, rondes, règle, description): crée un nouveau tournoi",
                         "(.M)odifier (T)ournoi (tournoi_id, joueur_id): modifie un tournoi, les joueurs inscrit par défaut",
                         "(.D)émarer (T)ournoi : clos les inscriptions de joueurs et permet de démarer les rondes",
                         "(.V)alider (T)ournoi (tournoi_id): clos le tournoi",
                         "(.N)ouvelle (R)onde (tournoi_id, name): commence une nouvelle ronde",
                         "(.M)odifier (R)onde (tournoi_id, joueur_id, result): permet de modifier le résultat des matches",
                         "(.V)alider (R)onde (tournoi_id): termine la ronde"
                        ]
        self.rapports = ["(.L)iste (J)oueurs : ",
                         "(.L)iste (C)lassements : ",
                         "(.L)iste (T)ournois : ",
                         "(.L)iste (T)ournoi (J)oueurs : ",
                         "(.L)iste (T)ournoi (C)lassements : ",
                         "(.L)iste (T)ournoi (R)oundes : ",
                         "(.L)iste (T)ournoi (M)atchs : "
                        ]
        self.values = ["La commande et les valeurs doivent être séparés par un espace. Les valeurs sont séparées par des virgules.\n",
                       "Les valeurs peuvent être rentrées/modifiées à l'aide de clef et sont alors traitées en priorité 'ex: nom=Dupont.\n",
                       "Les valeurs entrés sans clef seront ensuite assignés dans l'ordre aux clef encore sans valeur (?).\n",
                       "Si la commande est entrée sans un nombre suffisant de valeurs l'utilisateur sera orienté vers un sous-menu.\n",
                       "Depuis un sous-menu, on peut entrer directement la ou les valeurs manquantes sans taper de commande.\n",
                       "Ou entrer directement n'importe quelle commande comme depuis le menu principal.\n"
                       ]



