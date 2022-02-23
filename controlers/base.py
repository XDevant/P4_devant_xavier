from controlers.selector import Selector
from controlers.state import State
from controlers.language import command_translation
from models.feedback import Feedback


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.state = State()

    def run(self):
        running = True
        while running:
            feedback = Feedback()
            if self.state.validation:
                feedback.input = self.view.gather_confirmation(self.state.default_command)
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
                getattr(self.selector, feedback.command).parse_values(feedback, self.state)
            else:
                self.view.command_error(feedback)
                continue
            if feedback.parsed:
                try:
                    getattr(self.selector, feedback.command).execute(feedback, self.db, self.state)
                except Exception as err:
                    self.view.execution_error(feedback)
                else:
                    next_command = self.state.default_command
                    if next_command is not None and next_command != feedback.command:
                        self.state.prediction = True
                        feedback.next_command = next_command
                        getattr(self.selector, next_command).parse_values(feedback, self.state)
                        self.state.prediction = False
                    self.view.display(feedback)
            else:
                if feedback.command == self.state.last_command:
                    self.view.muted = True
                else:
                    self.view.muted = False
                self.view.parsing_error(feedback)

            if feedback.command == "quit":
                        running = False
            self.state.ignore_default = False


    def parse_input(self, feedback):
        if feedback.input == "..":
            return ("..", [])
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
