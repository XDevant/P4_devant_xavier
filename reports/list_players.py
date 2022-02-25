from commands.command import Command
from models.player import Player


class ListPlayers(Command):
    def __init__(self):
        self.commands = ["lj", "lp"]
        self.natural = [["liste", "joueurs", "list", "players"]]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None

    def execute(self, feedback, db, state):
        table = db.table("players")
        players = sorted(table.all(), key=lambda player: player['last_name'] + player['first_name'])
        feedback.title = "Rapport: Liste des Joueurs (alphabétique)"
        feedback.data = [Player(**player) for player in players]
        return None
