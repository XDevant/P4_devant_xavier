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
        return new_dict, errors

    def execute(self, values, db, state):
        feedback = {}
        tournament = Tournament(db, **db.table("tournaments").get(doc_id=values['tournament_id']))
        feedback["rounds"] = tournament.round_details
        feedback["title"] = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Matches"
        return feedback