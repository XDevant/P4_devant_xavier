from commands.command import Command
from models.player import Player


class ListRanks(Command):
    def __init__(self):
        self.commands = ["lc", "lk"]
        self.natural = [["liste", "classement", "list", "ranking"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.parsed =True
        return None


    def execute(self, feedback, db, state):
        table = db.table("players")
        players = sorted(table.all(), key=lambda player: player['ranking'])
        feedback.title = "Rapport: Liste des Joueurs (classement)"
        feedback.data = [Player(**player) for player in players]
        return None