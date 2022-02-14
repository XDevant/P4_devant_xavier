from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament



class UpdateRound(Command):
    def __init__(self):
        self.commands = (".ra", ".ru")
        self.natural = [["ronde", "actualiser", "round", "update"]]
        self.values = {"tournament_id": None, "player_id": None, "score": None}


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        new_dict = self.values
        saved_dict = state.round_update_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        return int(value) > 0


    def execute(self, raw_command, values, db, state):
        name = "Nouveau résultat:"
        table = db.table("tournaments")
        tournament = table.get(doc_id=values['tournament_id'])
        tournament = Tournament(db, **tournament)
        round = tournament.round_details[-1]
        i, j = round.find_indexes(values["player_id"])
        if i < 0:
            return "Joueur non inscrit", []
        if j == 0:
            points_a = values["score"]
            if round.matches[i][1][1] is None:
                points_b = 1 - values["score"]
            else:
                points_b = round.matches[i][1][1]
        else:
            points_b = values["score"]
            if round.matches[i][0][1] is None:
                points_a = 1 - values["score"]
            else:
                points_a = round.matches[i][0][1]
        round.update_match(i, points_a, points_b)
        tournament.round_details[-1] = round
        tournament.complete_update(db)
        return name, [tournament]
