from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        self.commands = ()
        self.natural = ()

    @abstractmethod
    def is_the_one(self, input):
        if input.startswith(self.commands):
            print("is_the_one")
            return True
        
        return False

    @abstractmethod
    def parse_values(self):
        print("parsing value")


    @abstractmethod
    def execute(self, input):
        print("Sauvé")