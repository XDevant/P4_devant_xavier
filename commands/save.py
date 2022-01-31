class Save():
    def __init(self):
        self.commands = [".s", ".e"]
        self.natural = ["sauver", "save", "enregistrer"]

    def execute(self, input):
        if input.startswith('.s'):
            print("Sauvé !")
            return True
        return False