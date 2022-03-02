from commands.command import Command
from controlers.state import State

class Reset(Command):
    def __init__(self):
        self.commands = ["r"]
        self.keys = []
        self.values = []

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None

    def execute(self, feedback, db, state):
        feedback.success = True
        feedback.title = "Réinitialisation du programme:"
        feedback.data = ["L'êtat du programme est Réinitialisé"]
        state = State()
        state.last_command = feedback.command
        return None
