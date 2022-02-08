from commands.command import Command
from db_models.player import Player


class Playerlist(Command):
    def __init__(self):
        self.commands = (".lj", ".lp", ".lc", ".lr")
        self.natural = [["list", "joueur", "player", "classement", "ranking"]]
        self.values = None
        self.name = "Liste des Joueurs"
        self.ranking = False


    def is_the_one(self, input):
        if input.startswith(self.commands):
            if input.startswith(self.commands[2:]):
                self.ranking = True
            values = input.split(' ')[-1]
            return True, values
        
        return False, input


    def parse_values(self, input):
        return super().parse_values(input)


    def execute(self, input, db):
        players_table = db.table("players")
        if self.ranking:
            players = sorted(players_table.all(), key=lambda player: player['ranking'])
            name = self.name + " (classement)"
        else:
            players = sorted(players_table.all(), key=lambda player: player['last_name'] + player['first_name'])
            name = self.name + " (alphabétique)"
        return name, [Player(**player) for player in players]