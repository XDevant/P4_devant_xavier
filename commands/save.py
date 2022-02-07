from commands.command import Command


class Save(Command):
    def __init__(self):
        self.commands = (".s", ".e")
        self.natural = [["sauver", "save", "enregistrer"]]
        self.values = None


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self):
        return super().parse_values()


    def execute(self, input):
        print("Sauvé?")
        return super().execute(input)