from commands.command import Command
from db_models.player import Player


class NewPlayer(Command):
    def __init__(self):
        self.commands = (".nj", ".np", ".jn", ".pn")
        self.natural = [["nouveau", "new"], ["joueur", "player"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        dict = {"last_name": None, "first_name": None, "date_of_birth": None, "gender": None, "ranking": 'auto'}
        saved_dict = state.new_player
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if check:
            return new_dict, errors
        else:
            state.menu = "new_player"
            state.default_command = "new_player"
            state.next_key = errors[-1]
            state.new_player = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors



    def execute(self, raw_command, values, db, state):
        name = "Nouveau Joueur crée:"
        new_item = Player(**values)
        new_item.register(db.table("players"))
        state.default_player = new_item.id
        state.new_player = {}
        state.menu = None
        state.default_command = None
        state.last_command = "new_player"
        state.next_key = None
        return name, [new_item]