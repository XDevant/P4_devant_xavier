from commands.command import Command


class Quit(Command):
    def __init__(self):
        self.commands = (".q", ".x")
        self.natural = [["quitter", "exit", "close", "fermer"]]
        self.values = None


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        return super().parse_values(raw_command, raw_values, state)


    def execute(self, raw_command, values, db, state):
        print("Sauvé?")
        return super().execute(raw_command, values, db, state)