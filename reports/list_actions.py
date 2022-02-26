from commands.command import Command


class ListActions(Command):
    def __init__(self):
        self.commands = ["la", "al"]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None

    def execute(self, feedback, db, state):
        feedback.title = "Rapport: Liste des Actions"
        feedback.succes = True
        return None
