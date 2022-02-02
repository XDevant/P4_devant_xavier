from commands.command import Command


class Quit(Command):
    def __init__(self):
        self.commands = (".q", ".x")
        self.natural = ("quitter", "exit", "close", "fermer")


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self):
        print("parsing value")


    def execute(self, input):
        if input.startswith('.q'):
            print("Au revoir")
            return True
        return False