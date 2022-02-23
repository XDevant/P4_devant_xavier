from reports.list_tournament_players import ListTournamentPlayers
from models.tournament import Tournament


class ListTournamentRounds(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltr")
        self.natural = [["liste", "tournoi", "rondes", "list", "tournament", "rounds"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        super().parse_values(feedback.raw_values, state)
        state.default_command = "list_tournament_rounds"
        return None

    def execute(self, feedback, db, state):
        stringified_tournament = db.table("tournaments").get(doc_id=feedback.values["tournament_id"])
        if stringified_tournament is None:
            feedback.title = f"Rapport: Tournoi, Liste des Joueurs"
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            tournament = Tournament(db, **stringified_tournament)
            rounds = tournament.round_details
            feedback.title = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Rondes"
            if len(rounds) > 0:
                feedback.data = [round.name for round in rounds]
            else:
                feedback.data = ["Aucun round trouvé pour ce tournoi"]

        state.default_command = None
        state.next_key = None
        return None