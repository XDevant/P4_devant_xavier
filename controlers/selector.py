import commands

class Selector:
    """For each command class in commands, init sets a selectors attribute named after the command name
    equal to an instance of the command class. Equivalent to self.command_name = Command_name()
    """
    def __init__(self):
        self._command_list = [command for command in dir(commands) if command.istitle()]
        for command in self._command_list:
            setattr(self, command.lower(), getattr(commands, command)())

    def __iter__(self):
        for command in self._command_list:
            yield command.lower()

    


    