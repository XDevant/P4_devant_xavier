import commands

class Selector:
    """For each command class in the commands package, init sets a selectors attribute named after the command name
    equal to an instance of the command class. Equivalent to self.command_name = Command_name()
    """
    def __init__(self):
        self.command_list = [command.lower() for command in dir(commands) if command.istitle()]
        for command in self.command_list:
            setattr(self, command, getattr(commands, command.title())())

    def __iter__(self):
        return self.command_list.__iter__()



    
    