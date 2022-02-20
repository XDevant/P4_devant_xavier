from commands.command import Command
from db_models.player import Player


class ListRanks(Command):
    def __init__(self):
        self.commands = ("lc", "lk")
        self.natural = [["liste", "classement", "list", "ranking"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        return super().parse_values(raw_values, state)


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        table = db.table("players")
        players = sorted(table.all(), key=lambda player: player['ranking'])
        feedback["title"] = "Rapport: Liste des Joueurs (classement)"
        feedback["data"] = [Player(**player) for player in players]
        return feedback