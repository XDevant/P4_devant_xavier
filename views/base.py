from views.help import Help
from views.report import Report

class View:
    def __init__(self):
        self.help = Help()
        self.report = Report()

    def gather_command(self):
        answer = input()
        return answer

    def command_error(self, input):
        print(f"Aucune commande trouvé pour {input}")
        return None

    def parsing_error(self, input, command, values):
        print(f"Valeurs fournies incompatibles avec la commande: {command} + {values}")
        return None

    def execution_error(self, input, command, values):
        print(f"Erreur lors de l'execution de la commande: {command} + {values}")
        return None

    def display(self, name, data):
        print(name)
        for item in data:
            print(item)
        return None