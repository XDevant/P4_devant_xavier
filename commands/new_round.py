from commands.command import Command
from db_models.tournament import Tournament
from db_models.round import Round


class StartTournament(Command):
    def __init__(self):
        self.commands = (".rd", ".rs")
        self.natural = [["ronde", "démarrer", "round" "start"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is not None:
            values = {"name": raw_values[0].split('=')[-1]}
            if len(values["name"]) > 0:
                return True, values
        return True, {"name": "Round "}

    def execute(self, raw_command, values, db, state):
        pass