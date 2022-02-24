from commands.command import Command


class Save(Command):
    def __init__(self):
        self.commands = ["s", "e"]
        self.natural = [["sauver", "save", "enregistrer"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None


    def execute(self, feedback, db, state):
        return None