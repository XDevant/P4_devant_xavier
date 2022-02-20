from controlers.selector import Selector
from controlers.state import State
from controlers.language import command_translation


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.state = State()

    def run(self):
        running = True
        while running:
            if self.state.default_command is None:
                input = self.view.gather_command()
                raw_command, raw_values = self.parse_input(input)
            else:
                input = self.view.gather_value(self.state.next_key)
                raw_command, raw_values = self.parse_input(input)
            if raw_command is None:
                if self.state.default_command is None:
                    command = None
                else:
                    command = self.state.default_command
            else:
                command = self.find_command(raw_command)

            if command:
                values, errors = getattr(self.selector, command).parse_values(raw_values, self.state)
            else:
                self.view.command_error(input)
                continue

            if errors[-1] == []:
                try:
                    feedback = getattr(self.selector, command).execute(values, self.db, self.state)
                except Exception as err:
                    print(type(err))
                    self.view.execution_error(command, values, errors)
                else:
                    self.view.display(feedback)
            else:
                if command == self.state.last_command:
                    self.view.muted = True
                else:
                    self.view.muted = False
                self.view.parsing_error(command, values, errors)

            if command == "quit":
                        running = False
            if self.state.ignore_default:
                 self.state.ignore_default = False


    def parse_input(self, input):
        if input == "..":
            return ("..", [])
        base = 0
        splited_input = input.split(' ')
        if input.startswith('..'):
            self.state.ignore_default = True
        if input.startswith('.') or self.state.default_command is None:
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
        return (raw_command, raw_values)


    def find_command(self, raw_command):
        if raw_command:
            for command in self.selector:
                result = getattr(self.selector, command).is_the_one(raw_command)
                if result:
                    return command
        return None
