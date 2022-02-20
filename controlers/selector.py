import commands
from controlers.language import command_translation


class Selector:
    """For each command class in the commands package, init sets a selectors attribute named after the command name
    equal to an instance of the command class. Equivalent to self.command_name = CommandName()
    """
    def __init__(self):
        self.class_list = [command for command in dir(commands) if command[0].isupper()]
        self.command_list = []
        for command_class in self.class_list:
            command = command_translation[command_class.lower()][-1]
            self.command_list.append(command)
            setattr(self, command, getattr(commands, command_class)())

    def __iter__(self):
        return self.command_list.__iter__()



    
    