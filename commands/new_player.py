from commands.command import Command
from models.player import Player


class NewPlayer(Command):
    def __init__(self):
        self.commands = ["nj", "np", "jn", "pn"]
        self.natural = [["nouveau", "new"], ["joueur", "player"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.values = {"last_name": None, "first_name": None, "date_of_birth": None, "gender": None, "ranking": 'auto'}
        saved_dict = state.new_player
        self.load_values(feedback, saved_dict)
        if feedback.parsed:
            return None
        else:
            state.parsing_failure(feedback)
            return None



    def execute(self, feedback, db, state):
        new_item = Player(**feedback.values)
        new_item.register(db.table("players"))

        state.execute_succes(feedback)
        state.default_command = None

        feedback.title = "Nouveau Joueur crée:"
        feedback.data = [new_item]
        return None