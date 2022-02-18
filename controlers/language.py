key_translation = {"name": ["nom", "name"],
                   "first_name": ["prénom", "first name", "prenom"],
                   "last_name": ["nom", "last name", "name"],
                   "date": ["date", "date"],
                   "date_of_birth": ["date de naissance", "date of birth", "date"],
                   "score": ["score"],
                   "ranking": ["classement", "ranking", "rang", "rank"],
                   "gender": ["genre", "gender"],
                   "rounds": ["rondes", "rounds"],
                   "id": ["identifiant", "id",  "joueur", "player", "tournoi", "tournament", "round", "ronde"],
                   "player_id": ["joueur", "player", "identifiant", "id"],
                   "tournament_id": ["tournoi", "tournament", "identifiant", "id"]
                  }

command_translation = {"newplayer": ["Nouveau Joueur", "New Player"],
                       "newtournament": ["Nouveau Tournoi", "New Tournament"],
                       "newround": ["Nouvelle Ronde", "New Round"],
                       "updateplayer": ["Modifier Joueur", "Update Player"],
                       "updatetournament": ["Modifier Tournoi", "Update Tournament"],
                       "updateround": ["Modifier Round", "Update Round"],
                       "starttournament": ["Démarrer Tournoi", "Start Tournament"],
                       "startround": ["Démarrer Ronde", "Start Round"],
                       "help": ["Aide", "Help"],
                       "save": ["Sauver", "Save"],
                       "quit": ["Quitter", "eXit"],
                       "options": ["Options", "Options"],
                       "reset": ["Réinitialiser", "Reset"]
                      }

class Translation:
    def __init__(self):
        self.keys = key_translation
        self.commands = command_translation