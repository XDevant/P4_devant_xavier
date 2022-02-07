from commands.command import Command


class PlayerList(Command):
    def __init__(self):
        self.commands = (".lj", ".lp")
        self.natural = [["list", "joueur", "player"]]
        self.values = None


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self):
        return super().parse_values()


    def execute(self):
        print("Sauvé")