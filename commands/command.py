from abc import ABC, abstractmethod
from controlers.language import key_translation
from models.tournament import Tournament


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
                    error = f"Clef incorecte: {new_key} pour valeur {value}"
                    feedback.errors.append(error)
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
            error = f"Valeur incorrecte pour {key}: {value}"
            error += ", attendu entier positif"
            return check,  error
        if key == "score":
            if str(value) in ["0", "D"]:
                return True, 0
            if str(value) in ["1", "V"]:
                return True, 1
            if str(value) in ["0.5", "N", "1/2"]:
                return True, 0.5
            error = f"Valeur incorrecte pour {key}: {value}"
            error += ", attendu 0, 1, 0.5, V, D, N, 1/2"
            return False,  error
        elif "date" in key:
            return True, value
        elif key == "rule":
            if value.lower() in ["blitz", "bullet", "coup rapide"]:
                return True, value
            error = f"Valeur incorrecte pour {key}: {value}"
            error += ", attendu blitz, bullet ou coup rapide"
            return False, error
        else:
            if len(value) > 0:
                return True, value
        return False, f"Valeur incorrecte pour {key}: {value}"

    def load_tournament(self, feedback, db, state):
        table = db.table("tournaments")
        tournament_id = feedback.values["tournament_id"]
        stringified_tournament = table.get(doc_id=tournament_id)
        if stringified_tournament is None:
            feedback.important = f"Le tournoi {tournament_id} n'existe pas!"
            return None
        return Tournament(db, **stringified_tournament)

    def check_start(self, feedback, state, tournament):
        check_1 = len(tournament.players) % 2 != 0
        check_2 = len(tournament.players) <= tournament.rounds
        if tournament.round == 0 and (check_1 or check_2):
            feedback.title = "Démarrer Tournoi:"
            feedback.important = "Nombre d'inscrits impair ou insuffisant!"
            state.default_command = "update_tournament"
            state.default_tournament = tournament.id
            return False
        return True

    def check_end_round(self, feedback, state, tournament):
        if len(tournament.round_details) == 0:
            missing = False
        else:
            missing = tournament.round_details[-1].chech_matches() >= 0
        if tournament.round > 0 and missing:
            feedback.title = "Démarrer Nouveau Round:"
            feedback.important = "Echec! La ronde actuelle n'est pas terminée!"
            state.default_command = "update_tournament"
            state.active_tournament = tournament.id
            return False
        return True

    def check_ended(self, feedback, state, tournament):
        if tournament.finished:
            feedback.title = "Démarrer Nouveau Round:"
            feedback.important = "Tournoi déja terminé"
            state.default_command = None
            state.active_tournament = None
            return False
        return True

    def can_start(self, feedback, tournament):
        check_1 = len(tournament.players) % 2 != 0
        check_2 = len(tournament.players) <= tournament.rounds
        if tournament.round == 0 and (check_1 or check_2):
            feedback.important = "Nombre d'inscrits impair ou insuffisant!"
            return False
        feedback.important = "Nombre d'inscrits pair et suffisant! "
        feedback.important += "Entrez .dt pour démarrer le tournoi. "
        return True