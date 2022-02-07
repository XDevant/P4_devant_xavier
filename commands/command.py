from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self.commands = ()
        self.natural = [[]]
        self.values = None


    @abstractmethod
    def is_the_one(self, input):
        if input.startswith(self.commands):
            values = input.split(' ')[-1]
            return True, values
        
        return False, input

    @abstractmethod
    def parse_values(self, input):
        if not self.values:
            return True, {}

    @abstractmethod
    def execute(self, input, db):
        print("Sauvé")
        return True, None