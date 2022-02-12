from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament


class New(Command):
    def __init__(self):
        self.commands = (".nj", ".np", ".nt")
        self.natural = [["nouveau", "joueur", "tournoi", "new", "player", "tournament"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        check = True
        if 't' in raw_command:
            new_dict = {"name": None, "place": None, "date": None, "description": None, "rule": None, "rounds": 4}
            saved_dict = state.tournament_in_process
        else:
            new_dict = {"last_name": None, "first_name": None, "date_of_birth": None, "gender": None, "ranking": 'auto'}
            saved_dict = state.player_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        if key == "ranking" or key == "rounds":
            return value.isnumeric() and int(value) > 0
        elif "date" in key:
            return True
        else:
            return len(value) > 0


    def execute(self, raw_command, values, db, state):
        if 't' in raw_command:
            name = "Nouveau Tournoi:"
            new_item = Tournament(**values)
            table = db.table("tournaments")
        else:
            name = "Nouveau Joueur:"
            new_item = Player(**values)
            table = db.table("players")
        new_item.register(table)
        return name, [new_item]