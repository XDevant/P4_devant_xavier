import commands

class Selector:
    def __init__(self):
        self.save = commands.Save()

    def talk_to_me(self, topic):
        self.save.execute("bouh")
        print(dir(commands))
        return 1