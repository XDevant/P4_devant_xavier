import commands

class Selector:
    def __init__(self, *args):
        for command in args:
            setattr(self, command.lower(), getattr(commands, command)())

    