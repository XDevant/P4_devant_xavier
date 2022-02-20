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

command_translation = {"newplayer": ["Nouveau Joueur", "New Player", "new_player"],
                       "newtournament": ["Nouveau Tournoi", "New Tournament", "new_tournament"],
                       "newround": ["Nouvelle Ronde", "New Round", "new_round"],
                       "updateplayer": ["Modifier Joueur", "Update Player", "update_player"],
                       "updatetournament": ["Modifier Tournoi", "Update Tournament", "update_tournament"],
                       "updateround": ["Modifier Round", "Update Round", "update_round"],
                       "starttournament": ["Démarrer Tournoi", "Start Tournament", "start_tournament"],
                       "startround": ["Démarrer Ronde", "Start Round", "start_round"],
                       "help": ["Aide", "Help", "help"],
                       "save": ["Sauver", "Save", "save"],
                       "quit": ["Quitter", "eXit", "quit"],
                       "options": ["Options", "Options", "options"],
                       "reset": ["Réinitialiser", "Reset", "reset"],
                       "report": ["Rapport", "Report", "report"]
                      }


class Translation:
    def __init__(self):
        self.keys = key_translation
        self.commands = command_translation