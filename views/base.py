from views.help import Help
from views.report import Report
from controlers.language import Translation

class View:
    def __init__(self):
        self.verbose = True
        self.examples = True
        self.muted = False
        self.help = Help()
        self.report = Report()
        self.translation = Translation()

    def gather_command(self):
        answer = input("\nEntrez une commande: ")
        return answer


    def gather_value(self, next_key):
        message = f"\nEntrez un(e) {self.translation.keys[next_key][0]}: "
        answer = input(message)
        return answer


    def command_error(self, input):
        print(f"Aucune commande trouvé pour {input}")
        return None


    def parsing_error(self, command, values, errors):
        print(f"\n Valeurs fournies insuffisantes pour la commande: {self.translation.commands[command][0]}")
        if len(errors) > 1:
            print(*errors[:-1])
        display_values = {}
        for key, value in values.items():
            if value is None:
                value = "?"
            display_values[self.translation.keys[key][0]] = value
        print("\n Valeurs actuelles:", display_values)
        if self.verbose and not self.muted:
            print(*self.help.values[:3])
        return None

    def execution_error(self, command, values, errors):
        print(f"Erreur lors de l'execution de la commande: {command} + {values}")
        return None

    def display(self, name, data):
        print("\n", name)
        for item in data:
            print(item)
        return None