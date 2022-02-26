import commands
import reports


class Selector:
    """
    For each command class in the commands package, init sets an attribute
    named after the command name equal to an instance of the command class.
    Equivalent to self.command_name = CommandName()
    """
    def __init__(self):
        self.commands = []
        command_classes = [com for com in dir(commands) if com[0].isupper()]
        report_classes = [rep for rep in dir(reports) if rep[0].isupper()]
        for command_class in command_classes:
            command = self.snake_to_under(command_class)
            self.commands.append(command)
            setattr(self, command, getattr(commands, command_class)())
        for report_class in report_classes:
            report = self.snake_to_under(report_class)
            self.commands.append(report)
            setattr(self, report, getattr(reports, report_class)())

    def __iter__(self):
        return self.commands.__iter__()

    def snake_to_under(self, snake):
        under = snake[0].lower()
        if len(snake) == 0:
            return snake
        under = snake[0].lower()
        if len(snake) == 1:
            return under
        for char in snake[1:]:
            if char.isupper():
                under += "_"
            under += char.lower()
        return under
