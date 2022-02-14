from commands.command import Command
from db_models.player import Player


class NewPlayer(Command):
    def __init__(self):
        self.commands = (".nj", ".np")
        self.natural = [["nouveau", "joueur", "new", "player"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        new_dict = {"last_name": None, "first_name": None, "date_of_birth": None, "gender": None, "ranking": 'auto'}
        saved_dict = state.player_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        if key == "ranking":
            return value.isnumeric() and int(value) > 0
        elif "date" in key:
            return True
        else:
            return len(value) > 0


    def execute(self, raw_command, values, db, state):
        name = "Nouveau Joueur:"
        new_item = Player(**values)
        new_item.register(db.table("players"))
        return name, [new_item]