from reports.list_tournament_players import ListTournamentPlayers
from db_models.tournament import Tournament


class ListTournamentMatchs(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltm")
        self.natural = [["liste", "tournoi", "matches", "list", "tournament", "matches"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        new_dict, errors = super().parse_values(raw_values, state)
        state.default_command = "list_tournament_matchs"
        state.next_key = "tournament_id"
        return new_dict, errors

    def execute(self, values, db, state):
        feedback = {}
        stringified_tournament = db.table("tournaments").get(doc_id=values["tournament_id"])
        if stringified_tournament is None:
            feedback["title"] = f"Rapport: Tournoi, Liste des Matches"
            feedback["data"] = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            tournament = Tournament(db, **stringified_tournament)
            feedback["title"] = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Matches"
            rounds = tournament.round_details
            if len(rounds) > 0:
                feedback["data"] = rounds
            else:
                feedback["data"] = ["Aucun round trouvé pour ce tournoi"]

        state.default_command = None
        state.next_key = None
        return feedback