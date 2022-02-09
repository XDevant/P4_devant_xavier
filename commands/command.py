from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self.commands = ()
        self.natural = [[]]
        self.values = None


    @abstractmethod
    def is_the_one(self, input):
        if input.startswith(self.commands):
            return True
        return False

    @abstractmethod
    def parse_values(self, raw_command, raw_values, state):
        if not self.values:
            return True, {}

    @abstractmethod
    def execute(self, raw_command, values, db, state):
        return True, None