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
        self.language = 0

    def gather_command(self):
        answer = input("\nEntrez une commande: ")
        return answer


    def gather_value(self, next_key):
        if next_key is None:
            message = f"\nEntrez la/les valeur(s) manquante(s): "
        else:
            message = f"\nEntrez un(e) {self.translation.keys[next_key][self.language]}: "
        answer = input(message)
        return answer


    def command_error(self, input):
        print(f"Aucune commande trouvé pour {input}")
        return None


    def parsing_error(self, command, values, errors):
        pretty_command = self.translation.commands[command][self.language]
        print(f"\n Valeurs fournies insuffisantes pour la commande: {pretty_command}")
        if self.verbose and not self.muted:
            print(*self.help.values[:3])
        if len(errors) > 1:
            print(*errors[:-1])
        display_values = {}
        for key, value in values.items():
            if value is None:
                value = "?"
            display_values[self.translation.keys[key][self.language]] = value
        print("Valeurs actuelles: ", display_values, "\n ")
        return None

    def execution_error(self, command, values, errors):
        print(f"Erreur lors de l'execution de la commande: {command} + {values}")
        return None

    def display(self, feedback):
        print("\n", feedback["title"])
        for item in feedback["data"]:
            print(item)
        for key, value in feedback.items():
            if key not in ["title", "data"] and len(value) > 0:
                print(value)
        return None