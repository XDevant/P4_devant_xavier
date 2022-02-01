import commands

class Selector:
    def __init__(self):
        command_list = [command for command in dir(commands) if command.istitle()]
        for command in command_list:
            setattr(self, command.lower(), getattr(commands, command)())

    