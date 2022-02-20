import commands
import reports


class Selector:
    """For each command class in the commands package, init sets a selectors attribute named after the command name
    equal to an instance of the command class. Equivalent to self.command_name = CommandName()
    """
    def __init__(self):
        self.commands = []
        command_classes = [command for command in dir(commands) if command[0].isupper()]
        report_classes = [report for report in dir(reports) if report[0].isupper()]
        for command_class in command_classes + report_classes:
            command = self.snake_to_under(command_class)
            self.commands.append(command)
            setattr(self, command, getattr(commands, command_class)())

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

    
    