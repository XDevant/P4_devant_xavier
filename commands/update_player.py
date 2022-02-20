from commands.command import Command
from db_models.player import Player


class UpdatePlayer(Command):
    def __init__(self):
        self.commands = ( "mj","jm","pu", "up")
        self.natural = [["joueur", "modifier", "player""update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"player_id": state.default_player, "ranking": None}
        saved_dict = state.update_player
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if check:
            return new_dict, errors
        else:
            state.default_command = "update_player"
            state.next_key = errors[-1]
            state.update_player = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors



    def execute(self, values, db, state):
        name = "Nouveau classement:"
        table = db.table("players")
        new_item = Player(**table.get(doc_id=values['player_id']))
        new_item.ranking = values["ranking"]
        new_item.complete_update(table)

        if "ranking" in values.keys():
            state.default_player = None
        state.update_player = {}
        state.default_command = None
        state.last_command = "update_player"
        state.next_key = None

        feedback = super().execute( values, db, state)
        feedback["name"] = "Nouveau classement:"
        feedback["data"] = [new_item]
        return feedback
