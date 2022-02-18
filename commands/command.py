from abc import ABC, abstractmethod


input_key_translation = {"name": ["nom", "name"],
                         "first_name": ["prénom", "first name", "prenom"],
                         "last_name": ["nom", "name", "last name"],
                         "date": ["date"],
                         "date_of_birth": ["date de naissance", "date of birth"],
                         "score": ["score"],
                         "ranking": ["classement", "rang", "rank", "ranking"],
                         "gender": ["genre", "gender"],
                         "rounds": ["rondes", "rounds"],
                         "id": ["identifiant", "id",  "joueur", "player", "tournoi", "tournament", "round", "ronde"],
                         "player_id": ["identifiant", "id", "joueur", "player"],
                         "tournament_id": ["identifiant", "id", "tournoi", "tournament"]
                         }

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
        if self.values is None:
            return True, {}

    @abstractmethod
    def execute(self, raw_command, values, db, state):
        return True, None

    
    def load_values(self, raw_values, new_dict, saved_dict):
        errors = []
        key_values = {}
        values = []
        for value in raw_values:
            if '=' in str(value):
                new_key, value = value.split('=')
                key = self.translate_key(new_key, new_dict.keys())
                if key is not None:
                    check, value = self.format_value(key, value)
                    if check:
                        key_values[key] = value
                    else:
                        errors.append(value)
                else:
                    errors.append(f"Clef incorecte: {new_key} pur valeur {value}")
            else:
                values.append(value)
        check = True
        for key in new_dict.keys():
            if key in key_values.keys():
                new_dict[key] = key_values[key]
                continue
            if key in saved_dict.keys():
                new_dict[key] = saved_dict[key]
                continue
            for i in range(len(values)):
                check, value = self.format_value(key, values[i])
                if check:
                    values.pop(i)
                    new_dict[key] = value
                    break
            if new_dict[key] is None:
                check = False
        return check, new_dict


    def translate_key(self, new_key, keys):
        for key in keys:
            if new_key.lower().strip() in input_key_translation[key]:
                return key
        return None


    def format_value(self, key, value):
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

