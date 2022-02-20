from reports.list_tournament_players import ListTournamentPlayers
from db_models.tournament import Tournament


class ListTournamentRounds(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltr")
        self.natural = [["liste", "tournoi", "rondes", "list", "tournament", "rounds"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        new_dict, errors = super().parse_values(raw_values, state)
        state.default_command = "list_tournament_rounds"
        return new_dict, errors

    def execute(self, values, db, state):
        feedback = {}
        tournament = Tournament(db, **db.table("tournaments").get(doc_id=values['tournament_id']))
        feedback["rounds"] = [round.name for round in tournament.round_details]
        feedback["name"] = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Rondes"
        return feedback