from commands.command import Command
from db_models.tournament import Tournament
from db_models.player import Player


class ListTournamentPlayers(Command):
    def __init__(self):
        self.commands = ("ltj", "ltp")
        self.natural = [["liste", "tournoi", "joueurs", "list", "tournament", "players"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"tournament_id": state.active_tournament}
        saved_dict = {}
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if check:
            return new_dict, errors
        else:
            state.default_command = "list_tournament_players"
            state.next_key = "tournament_id"
            return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        tournament = Tournament(db, **db.table("tournaments").get(doc_id=values["tournament_id"]))
        table = db.table("players")
        player_ids = tournament.players
        if player_ids == []:
            feedback["data"] = ["Aucun joueur inscrit en tournoi"]
        players = [table.get(doc_id=id) for id in player_ids]
        players.sort(key=lambda player: player['last_name'] + player['first_name'])
        feedback["name"] = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Joueurs"
        feedback["data"] = [Player(**player) for player in players]

        state.default_command = None
        state.next_key = None
        return feedback
