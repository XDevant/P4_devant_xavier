from commands.command import Command


class Quit(Command):
    def __init__(self):
        self.commands = ("q", "x")
        self.natural = [["quitter", "exit", "close", "fermer"]]
        self.values = None


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        if state.validation and feedback.raw_values != ['']:
            state.validation = False
            state.default_command = None
            feedback.success = True
            feedback.title = f"Quitter programme :"
            feedback.data = ["Commande annulée"]
        else:
            feedback.parsed = True
        return None


    def execute(self, feedback, db, state):
        if state.last_command == "save" and state.validation:
            state.validation = False
            feedback.title = "Quitter:"
            feedback.data = ["Vous quittez le programme"]
            state.default_command = None
        elif state.validation:
            state.validation = False
            feedback.title = "Quitter: confirmation"
            feedback.data = ["Vous quittez le programme sans sauver son êtat"]
            state.default_command = None
        else:
            feedback.title = "Veillez confirmer la commande Quitter.(Entrée)"
            feedback.info = "Vous pouver saisir n'importe quel autre caractère pour annuler."
            if state.last_command != "save":
                feedback.important = "Vous n'avez pas sauvegardé l'êtat du programme!"
                feedback.hint = "Si vous quiitez sans sauvegarde, les items en cours de création seront perdus."
            state.validation = True
            state.default_command = feedback.command
        feedback.success = True
        return None