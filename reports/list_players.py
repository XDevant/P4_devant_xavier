from commands.command import Command
from db_models.player import Player


class ListPlayers(Command):
    def __init__(self):
        self.commands = ("lj", "lp")
        self.natural = [["liste", "joueurs", "list", "players"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        return super().parse_values(raw_values, state)


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        table = db.table("players")
        players = sorted(table.all(), key=lambda player: player['last_name'] + player['first_name'])
        feedback["name"] = "Rapport: Liste des Joueurs (alphabétique)"
        feedback["data"] = [Player(**player) for player in players]
        return feedback