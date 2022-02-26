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

    def gather_value(self, keys):
        if keys is []:
            message = "\nEntrez la/les valeur(s) manquante(s): "
        else:
            pretty_keys = ', '.join([self.prettyfie_key(key) for key in keys])
            message = "\nEntrez " + pretty_keys + ": "
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
        message = f"Aucune commande trouvé pour {input}"
        print(message + ", entrez .la pour afficher la liste des actions possibles")
        return None

    def parsing_error(self, feedback):
        pretty_command = self.prettyfie_command(feedback.command)
        print(f"\n Valeurs fournies insuffisantes pour la commande: {pretty_command}")
        if len(feedback.errors) > 0:
            print(*feedback.errors)
        self.display_values("Valeurs actuelles: ", feedback.values)
        return None

    def execution_error(self, feedback):
        message = "Erreur lors de l'execution de la commande: "
        print(message + f"{feedback.command} + {feedback.values}")
        print("Entrez .la pour afficher la liste des actions possibles")
        return None

    def display(self, feedback):
        print("\n", feedback.title)
        if feedback.command == "list_actions":
            self.display_actions()
        else:
            for item in feedback.data:
                print(item)
            if feedback.info != "":
                print(feedback.info)
            if feedback.hint != "":
                print(feedback.hint)
            if feedback.important != "":
                print(feedback.important)
            if feedback.next_command is not None:
                self.display_menu(feedback)
        return None

    def display_menu(self, feedback):
        pretty_command = self.prettyfie_command(feedback.next_command)
        print(f"Menu {pretty_command}:")
        self.display_values("Valeurs actuelles: ", feedback.values)
        return None

    def display_menu_title(self, feedback):
        pretty_command = self.prettyfie_command(feedback.next_command)
        print(f"Menu {pretty_command}:")
        return None

    def display_values(self, name, values):
        display_values = {}
        for key, value in values.items():
            if value is None:
                value = "?"
            try:
                display_values[self.translation.keys[key][self.language]] = value
            except KeyError:
                display_values[key] = value
        print(name, display_values)
        return None

    def display_actions(self):
        for key, value in self.translation.commands.items():
            print(value[self.language])
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
