from reports.list_tournament_players import ListTournamentPlayers
from models.tournament import Tournament


class ListTournamentMatchs(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltm")
        self.natural = [["liste", "tournoi", "matches", "list", "tournament", "matches"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        super().parse_values(feedback.raw_values, state)
        state.default_command = feedback.command
        return None

    def execute(self, feedback, db, state):
        stringified_tournament = db.table("tournaments").get(doc_id=feedback.values["tournament_id"])
        if stringified_tournament is None:
            feedback.title = f"Rapport: Tournoi, Liste des Matches"
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            tournament = Tournament(db, **stringified_tournament)
            feedback.title = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Matches"
            rounds = tournament.round_details
            if len(rounds) > 0:
                feedback.data = rounds
            else:
                feedback.data = ["Aucun round trouvé pour ce tournoi"]

        state.default_command = None
        state.next_key = None
        return None