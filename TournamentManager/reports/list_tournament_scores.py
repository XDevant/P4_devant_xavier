from reports.list_tournament_players import ListTournamentPlayers
from controlers.sprite import TournamentSprite


class ListTournamentScores(ListTournamentPlayers):
    def __init__(self):
        self.commands = ["lts"]

    def is_the_one(self, input):
        if input in self.commands:
            return True
        return False

    def parse_values(self, feedback, state):
        super().parse_values(feedback, state)
        return None

    def execute(self, feedback, db, state):
        feedback.title = "Rapport: Tournoi, Cartes des Joueurs"
        tournament = self.load_tournament(feedback, db, state)
        if tournament is None:
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            active_tournament = TournamentSprite(tournament, db)
            active_tournament.sort_players("score")
            feedback.data = [active_tournament]
            feedback.succes = True
        state.default_command = None
        state.next_key = None
        return None
