class Quit():
    def __init(self):
        self.commands = [".q", ".x"]
        self.natural = ["quitter", "exit", "close", "fermer"]

    def execute(self, input):
        if input.startswith('.q'):
            print("Au revoir")
            return True
        return False