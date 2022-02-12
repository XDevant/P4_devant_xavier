import commands

class Selector:
    """For each command class in the commands package, init sets a selectors attribute named after the command name
    equal to an instance of the command class. Equivalent to self.command_name = Command_name()
    """
    def __init__(self):
        self.command_list = [command for command in dir(commands) if command[0].isupper()]
        for command in self.command_list:
            setattr(self, command.lower(), getattr(commands, command)())

    def __iter__(self):
        return self.command_list.__iter__()



    
    