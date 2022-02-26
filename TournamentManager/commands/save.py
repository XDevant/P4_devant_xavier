from commands.command import Command


class Save(Command):
    def __init__(self):
        self.commands = ["s", "e"]
        self.keys = []
        self.values = []
        self.next_command = "quit"

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None

    def execute(self, feedback, db, state):
        state.register(db)
        feedback.success = True
        feedback.title = "Sauver et Quitter:"
        feedback.data = ["L'êtat du programme est sauvegardé, tapez (Entrée) pour quitter"]
        feedback.info = "Vous pouver saisir n'importe quel autre caractère pour annuler."
        state.default_command = self.next_command
        state.last_command = feedback.command
        state.validation = True
        return None
