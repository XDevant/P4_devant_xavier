from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament


class NewTournament(Command):
    def __init__(self):
        self.commands = ("nt", "tn")
        self.natural = [["nouveau", "new"], ["tournoi", "tournament"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"name": None, "place": None, "date": None, "description": None, "rule": None, "rounds": 4}
        saved_dict = state.new_tournament
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if check:
            return new_dict, errors
        else:
            state.default_command = "new_tournament"
            state.next_key = errors[-1]
            state.new_tournament = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors


    def execute(self, values, db, state):
        new_item = Tournament(db, **values)
        new_item.register(db)
        state.default_tournament = new_item.id
        state.new_tournament = {}
        state.default_command = None
        state.last_command = "new_tournament"
        state.next_key = None
        
        feedback = super().execute( values, db, state)
        feedback["name"] = "Nouveau Tournoi crée:"  
        feedback["data"] = [new_item]
        return feedback