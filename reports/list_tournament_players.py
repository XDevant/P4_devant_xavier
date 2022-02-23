from commands.command import Command
from models.tournament import Tournament
from models.player import Player


class ListTournamentPlayers(Command):
    def __init__(self):
        self.commands = ("ltj", "ltp")
        self.natural = [["liste", "tournoi", "joueurs", "list", "tournament", "players"]]


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
            state.next_key = "tournament_id"
            return None


    def execute(self, feedback, db, state):
        stringified_tournament = db.table("tournaments").get(doc_id=feedback.values["tournament_id"])
        if stringified_tournament is None:
            feedback.title = f"Rapport: Tournoi {feedback.values['tournament_id']}, Liste des Joueurs"
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            tournament = Tournament(db, **stringified_tournament)
            table = db.table("players")
            player_ids = tournament.players
            feedback.title = f"Rapport: Tournoi {tournament.name} (n°{tournament.id}), Liste des Joueurs"
            if player_ids == []:
                feedback.data= ["Aucun joueur inscrit en tournoi"]
            else:
                players = [table.get(doc_id=id) for id in player_ids]
                players.sort(key=lambda player: player['last_name'] + player['first_name'])
                feedback.data = [Player(**player) for player in players]

        state.default_command = None
        state.next_key = None
        return None
