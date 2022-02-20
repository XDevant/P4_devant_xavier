key_translation = {"name": ["nom", "name"],
                   "first_name": ["prénom", "first name", "prenom"],
                   "last_name": ["nom", "last name", "name"],
                   "date": ["date", "date"],
                   "date_of_birth": ["date de naissance", "date of birth"],
                   "score": ["score"],
                   "ranking": ["classement", "ranking", "rang", "rank"],
                   "gender": ["genre", "gender"],
                   "rounds": ["rondes", "rounds"],
                   "id": ["identifiant", "id"],
                   "player_id": ["joueur", "player", "identifiant"],
                   "tournament_id": ["tournoi", "tournament", "identifiant"]
                  }

command_translation = {"new_player": ["Nouveau Joueur", "New Player"],
                       "new_tournament": ["Nouveau Tournoi", "New Tournament"],
                       "new_round": ["Nouvelle Ronde", "New Round"],
                       "update_player": ["Modifier Joueur", "Update Player"],
                       "update_tournament": ["Modifier Tournoi", "Update Tournament"],
                       "update_round": ["Modifier Round", "Update Round"],
                       "start_tournament": ["Démarrer Tournoi", "Start Tournament"],
                       "start_round": ["Démarrer Ronde", "Start Round"],
                       "help": ["Aide", "Help"],
                       "save": ["Sauver", "Save"],
                       "quit": ["Quitter", "eXit"],
                       "options": ["Options", "Options"],
                       "reset": ["Réinitialiser", "Reset"],
                       "list_players": ["Liste des Joueurs", "Player List"],
                       "list_ranks": ["Classement des Joueurs", "Player Ranking"],
                       "list_tournaments": ["Liste des Tournois", "Tournament List"],
                       "list_tournament_players": ["Liste des Joueurs en Tournoi", "Tournament Player List"],
                       "list_tournament_ranks": ["Classement des Joueurs en Tournoi", "Tournament Player Ranking"],
                       "list_tournament_rounds": ["Liste des Rounds du Tournoi", "Tournament Round List"],
                       "list_tournament_matchs": ["Liste des matches du Tournoi", "Tournament Match List"]
                      }


class Translation:
    def __init__(self):
        self.keys = key_translation
        self.commands = command_translation