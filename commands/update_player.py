from commands.command import Command
from db_models.player import Player


class UpdatePlayer(Command):
    def __init__(self):
        self.commands = (".ja",".pu")
        self.natural = [["joueur", "actualiser", "player""update"]]
        self.values = {"player_id": None, "ranking": None}


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        new_dict = self.values
        saved_dict = state.player_update_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        return int(value) > 0


    def execute(self, raw_command, values, db, state):
        name = "Nouveau classement:"
        table = db.table("players")
        new_item = Player(**table.get(doc_id=values['player_id']))
        new_item.ranking = values["ranking"]
        new_item.complete_update(table)
        return name, [new_item]
