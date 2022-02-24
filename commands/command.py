from abc import ABC, abstractmethod
from controlers.language import key_translation



class Command(ABC):
    def __init__(self):
        self.commands = []
        self.natural = [[]]


    @abstractmethod
    def is_the_one(self, input):
        if input in self.commands:
            return True
        return False

    @abstractmethod
    def parse_values(self, feedback, state):
        return None


    @abstractmethod
    def execute(self, feedback, db, state):
        return None

    
    def load_values(self, feedback, saved_dict):
        key_values = {}
        values = []
        for value in feedback.raw_values:
            if '=' in str(value):
                new_key, value = value.split('=')
                key = self.translate_key(new_key, feedback.values.keys())
                if key is not None:
                    check, value = self.format_value(key, value)
                    if check:
                        key_values[key] = value
                    else:
                        feedback.errors.append(value)
                else:
                    feedback.errors.append(f"Clef incorecte: {new_key} pour valeur {value}")
            else:
                values.append(value)
        check = True
        for key, value in feedback.values.items():
            if key in key_values.keys():
                feedback.values[key] = key_values[key]
                continue
            if key in saved_dict.keys():
                feedback.values[key] = saved_dict[key]
                continue
            if value is not None:
                continue
            for i in range(len(values)):
                validation, value = self.format_value(key, values[i])
                if validation:
                    values.pop(i)
                    feedback.values[key] = value
                    break
                else:
                    feedback.errors.append(value)
            if feedback.values[key] is None:
                feedback.next_keys.append(key)
                if check:
                    check = False
        for key, value in key_values.items():
            if key not in feedback.values.keys():
                feedback.values[key] = value
        feedback.parsed = check
        return None


    def translate_key(self, new_key, keys):
        for key in keys:
            if new_key.lower().strip() in key_translation[key] + [key]:
                return key
        return None


    def format_value(self, key, value):
        value = value.strip(' \'"')
        if key in ["rounds", "ranking", "id", "tournament_id", "player_id"]:
            check = value.isnumeric() and int(value) > 0
            if check:
                return check, int(value)
            return check,  f"Valeur incorrecte pour {key}: {value}, attendu entier positif"
        if key == "score":
            if str(value) in ["0", "D"]:
                return True, 0
            if str(value) in ["1", "V"]:
                return True, 1
            if str(value) in ["0.5", "N", "1/2"]:
                return True, 0.5
            return False,  f"Valeur incorrecte pour {key}: {value}, attendu 0, 1, 0.5, V, D, N, 1/2"
        elif "date" in key:
            return True, value
        elif key == "rule":
            if value.lower() in ["blitz", "bullet", "coup rapide"]:
                return True, value
            return False, f"Valeur incorrecte pour {key}: {value}, attendu blitz, bullet ou coup rapide"
        else:
            if len(value) > 0:
                return True, value
        return False, f"Valeur incorrecte pour {key}: {value}"

