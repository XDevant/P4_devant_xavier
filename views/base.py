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
            message = "\nEntrez la/les valeur(s) manquante(s): "
        else:
            message = f"\nEntrez un(e) {self.prettyfie_key(next_key)}: "
        answer = input(message)
        return answer


    def gather_confirmation(self, default_command):
        if default_command == "update_tournament":
            message = "\nEntree pour retirer le joueur du tournoi: "
        else:
            message = "\nEntree pour confirmer: "
        answer = input(message)
        return answer

    def command_error(self, input):
        print(f"Aucune commande trouvé pour {input}")
        return None


    def parsing_error(self, command, values, errors):
        pretty_command = self.prettyfie_command(command)
        print(f"\n Valeurs fournies insuffisantes pour la commande: {pretty_command}")
        if self.verbose and not self.muted:
            print(*self.help.values[:3])
        if len(errors) > 1:
            print(*errors[:-1])
        self.display_values(values)
        return None

    def execution_error(self, command, values, errors):
        print(f"Erreur lors de l'execution de la commande: {command} + {values}")
        return None

    def display(self, feedback):
        print("\n", feedback["title"])
        for item in feedback["data"]:
            print(item)
        for key, value in feedback.items():
            if key not in ["title", "data", "menu", "values"] and len(value) > 0:
                print(value)
        if "menu" in feedback.keys():
            self.display_menu(feedback["menu"], feedback["values"])
        return None


    def display_menu(self, command, values):
        pretty_command = self.prettyfie_command(command)
        print(f"Menu {pretty_command}:")
        self.display_values(values)
        return None


    def display_values(self, values):
        display_values = {}
        for key, value in values.items():
            if value is None:
                value = "?"
            try:
                display_values[self.translation.keys[key][self.language]] = value
            except KeyError:
                display_values[key] = value
        print("Valeurs actuelles: ", display_values)
        return None


    def prettyfie_command(self, command):
        try:
            pretty_command = self.translation.commands[command][self.language]
        except KeyError:
            pretty_command = command
        return pretty_command


    def prettyfie_key(self, key):
        try:
            pretty_key = self.translation.keys[key][self.language]
        except KeyError:
            pretty_key = key
        return pretty_key
