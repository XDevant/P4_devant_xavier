from commands.command import Command
from db_models.player import Player


class Playerlist(Command):
    def __init__(self):
        self.commands = (".lj", ".lp")
        self.natural = [["list", "joueur", "player"]]
        self.values = None


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, input):
        return super().parse_values(input)


    def execute(self, input, db):
        players_table = db.table("players")
        alpha_players = sorted(players_table.all(), key=lambda player: player['last_name'] + player['first_name'])
        return True, alpha_players