from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament



class UpdateRound(Command):
    def __init__(self):
        self.commands = ("mr", "rm", "ru", "ur")
        self.natural = [["ronde", "actualiser", "round", "update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"tournament_id": state.active_tournament, "player_id": None, "score": None}
        saved_dict = state.update_round
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if state.prediction:
                return new_dict, [[]]
        if check:
            return new_dict, errors
        else:
            state.default_command = "update_round"
            state.next_key = errors[-1]
            state.update_round = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
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

        state.update_round = {}
        state.last_command = "update_round"
        state.next_key = "player_id"
        if state.active_tournament != tournament.id:
            state.active_tournament = tournament.id
            feedback["info"] = f"Le tournoi n°{tournament.id} est le tournoi actif par default."

        feedback["title"] = "Nouveau résultat:"
        feedback["data"] = [tournament]
        return feedback
