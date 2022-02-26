from commands.command import Command
from models.player import Player


class ListTournamentPlayers(Command):
    def __init__(self):
        self.commands = ["ltj", "ltp"]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        if state.active_tournament is None:
            id = state.default_tournament
        else:
            id = state.active_tournament
        feedback.values = {"tournament_id": id}
        saved_dict = {}
        self.load_values(feedback, saved_dict)
        if feedback.parsed:
            return None
        else:
            state.default_command = feedback.command
            state.next_keys = ["tournament_id"]
            return None

    def execute(self, feedback, db, state):
        feedback.title = "Rapport: Tournoi, Liste des Matches"
        tournament = self.load_tournament(feedback, db, state)
        if tournament is None:
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            table = db.table("players")
            player_ids = tournament.players
            new_title = f" {tournament.name} (n°{tournament.id}),"
            splited_title = feedback.title.split(',')
            feedback.title = splited_title[0] + new_title + splited_title[0]
            if player_ids == []:
                feedback.data = ["Aucun joueur inscrit en tournoi"]
            else:
                players = [table.get(doc_id=id) for id in player_ids]
                players.sort(key=lambda p: p['last_name'] + p['first_name'])
                feedback.data = [Player(**player) for player in players]
                feedback.succes = True
        state.default_command = None
        state.next_key = None
        return None
