from commands.command import Command
from models.player import Player


class UpdatePlayer(Command):
    def __init__(self):
        self.commands = ( "mj","jm","pu", "up")
        self.natural = [["joueur", "modifier", "player""update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.values = {"player_id": state.default_player, "ranking": None}
        saved_dict = state.update_player
        self.load_values(feedback, saved_dict)
        if state.prediction:
                return None
        if feedback.parsed:
            return None
        else:
            state.default_command = "update_player"
            state.next_key = feedback.errors[-1]
            state.update_player = {key: value for key, value in feedback.values.items() if value is not None}
            return None



    def execute(self, feedback, db, state):
        table = db.table("players")
        new_item = Player(**table.get(doc_id=feedback.values['player_id']))
        new_item.ranking = feedback.values["ranking"]
        new_item.complete_update(table)

        if "ranking" in feedback.values.keys():
            state.default_player = None
        state.update_player = {}
        state.default_command = None
        state.last_command = "update_player"
        state.next_key = None
        feedback.title = "Nouveau classement:"
        feedback.data = [new_item]
        return None
