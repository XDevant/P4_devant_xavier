from commands.command import Command
from models.player import Player


class UpdatePlayer(Command):
    def __init__(self):
        self.commands = ["mj", "jm", "pu", "up"]
        self.natural = [["joueur", "modifier", "player""update"]]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.values = {"player_id": None, "ranking": None}
        saved_dict = state.update_player
        self.load_values(feedback, saved_dict)
        if state.prediction or feedback.parsed:
            return None
        else:
            state.parsing_failure(feedback)
            return None

    def execute(self, feedback, db, state):
        table = db.table("players")
        player_id = feedback.values['player_id']
        stringified_player = table.get(doc_id=player_id)
        print(stringified_player)
        if stringified_player is None:
            feedback.data = [f"Le jouer {player_id} n'existe pas!"]
            state.execute_refused(feedback, False)
            return None
        new_item = Player(**stringified_player)
        new_item.ranking = feedback.values["ranking"]
        new_item.complete_update(db)

        state.execute_succes(feedback)
        state.default_command = None

        feedback.title = "Nouveau classement:"
        feedback.data = [new_item]
        return None
