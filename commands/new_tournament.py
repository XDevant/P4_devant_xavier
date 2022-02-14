from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament


class NewTournament(Command):
    def __init__(self):
        self.commands = (".nt")
        self.natural = [["nouveau", "tournoi", "new", "tournament"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        check = True
        new_dict = {"name": None, "place": None, "date": None, "description": None, "rule": None, "rounds": 4}
        saved_dict = state.tournament_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        if key == "rounds":
            return value.isnumeric() and int(value) > 0
        elif "date" in key:
            return True
        elif key == "rule":
            return value.lower() in ["blitz", "bullet", "coup rapide"]
        else:
            return len(value) > 0


    def execute(self, raw_command, values, db, state):
        name = "Nouveau Tournoi:"
        new_item = Tournament(**values)
        new_item.register(db.table("tournaments"))
        return name, [new_item]