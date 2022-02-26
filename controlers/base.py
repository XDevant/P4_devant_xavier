from models.feedback import Feedback


class Controler:
    def __init__(self, db, selector, view, state):
        self.db = db
        self.view = view
        self.selector = selector
        self.state = state

    def start(self, new):
        feedback = Feedback()
        if new:
            feedback.title = "Bienvenue !"
            feedback.data = ['Entrez "la" pour afficherer la liste des action']
            self.view.display(feedback)
        else:
            feedback.title = "Bon retour, sauvegarde rechargée"
            feedback.data = ['Entrez ".." pour réinitialiser le programme']
            self.view.display(feedback)
            feedback.next_command = self.state.default_command
            try:
                feedback.values = getattr(self.state, feedback.next_command)
            except Exception:
                self.view.display_menu_title(feedback)
            else:
                self.view.display_menu(feedback)


    def run(self):
        while True:
            feedback = Feedback()
            if self.state.validation:
                default = self.state.default_command
                feedback.input = self.view.gather_confirmation(default)
            elif self.state.default_command is None:
                feedback.input = self.view.gather_command()
            else:
                feedback.input = self.view.gather_value(self.state.next_keys)
            self.parse_input(feedback)
            if feedback.raw_command is None:
                feedback.command = self.state.default_command
            else:
                feedback.command = self.find_command(feedback.raw_command)

            if feedback.command:
                args = self.selector, feedback.command
                getattr(*args).parse_values(feedback, self.state)
            else:
                self.view.command_error(feedback)
                continue

            if feedback.parsed:
                try:
                    args = self.selector, feedback.command
                    getattr(*args).execute(feedback, self.db, self.state)
                except Exception:
                    self.view.execution_error(feedback)
                    continue
            elif not feedback.success:
                if feedback.command == self.state.last_command:
                    self.view.muted = True
                else:
                    self.view.muted = False
                self.view.parsing_error(feedback)
                continue

            if self.state.default_command is not None and not self.state.validation:
                feedback.prepare_prediction(self.state)
                default = self.state.default_command
                getattr(self.selector, default).parse_values(feedback, self.state)
                feedback.post_prediction(self.state)
            self.view.display(feedback)

            if feedback.command == "quit" and not self.state.validation:
                break
            self.state.ignore_default = False

    def parse_input(self, feedback):
        if feedback.input == "..":
            return (".r", [])
        base = 0
        splited_input = feedback.input.split(' ')
        if feedback.input.startswith('..'):
            self.state.ignore_default = True
        if feedback.input.startswith('.') or self.state.default_command is None:
            raw_command = splited_input[0]
            if raw_command != ".":
                raw_command = raw_command.strip('.')
            base = 1
        else:
            raw_command = None
        if len(splited_input) > base:
            raw_values = ' '.join(splited_input[base:]).strip().split(',')
        else:
            raw_values = []
        feedback.raw_command = raw_command
        feedback.raw_values = raw_values
        return None

    def find_command(self, raw_command):
        if raw_command:
            for command in self.selector:
                result = getattr(self.selector, command).is_the_one(raw_command)
                if result:
                    return command
        return None
