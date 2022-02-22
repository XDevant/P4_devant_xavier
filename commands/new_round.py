from datetime import datetime
from commands.command import Command
from models.tournament import Tournament
from models.round import Round


class NewRound(Command):
    def __init__(self):
        self.commands = ("nr", "rd", "rs")
        self.natural = [["ronde", "démarrer", "round" "start"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"tournament_id": state.active_tournament, "name": None}
        saved_dict = state.new_round
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if (state.validation and raw_values == []) or state.prediction:
                return new_dict, [[]]
        if check:
            return new_dict, errors
        else:
            state.default_command = "new_round"
            state.next_key = errors[-1]
            state.new_round = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        table = db.table("tournaments")
        stringified_tournament = table.get(doc_id=values["tournament_id"])
        if stringified_tournament is None or "matches" not in state.new_round.keys():
            feedback["title"] = f"Nouvelle Ronde : Echec "
            if stringified_tournament is None:
                feedback["data"] = [f"Le tournoi {values['tournament_id']} n'existe pas!"]
            else:
                feedback["data"] = ["La ronde précédente n'est pas terminée!"]
            state.default_command = None
            state.next_key = None
            state.new_round = {}
            return feedback
        tournament = Tournament(db, **stringified_tournament)
        round = Round(name=values["name"], tournament=tournament.id)
        round.add_matches(*state.new_round["matches"])
        tournament.new_round(round)
        tournament.complete_update(db)
        state.default_command = "update_round"
        state.next_key = "player_id"
        state.last_command = "new_round"
        if state.active_tournament != tournament.id:
            state.active_tournament = tournament.id
            feedback["info"] = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
        feedback["title"] = "Nouvelle ronde démarrée:"
        feedback["data"] = [round]
        state.new_round = {}
        return feedback