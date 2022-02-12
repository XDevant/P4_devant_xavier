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

    
    def load_values(self, raw_values, new_dict, saved_dict):
        check = True
        key_values = {value.split('=')[0]: int(value.split('=')[1]) for value in raw_values if '=' in str(value)}
        raw_values = [int(value) for value in raw_values if '=' not in value]
        for key in new_dict.keys():
            if key in key_values.keys():
                if self.check_value(key, key_values[key]):
                    new_dict[key] = key_values[key]
                    continue
            if key in saved_dict.keys():
                new_dict[key] = saved_dict[key]
                continue
            for i in range(len(raw_values)):
                if self.check_value(key, raw_values[i]):
                    new_dict[key] = raw_values.pop(i)
                    break
            if new_dict[key] is None:
                check = False
        return check, new_dict


    def check_value(self, key, value):
        return True