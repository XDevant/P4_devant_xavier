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


    def parse_values(self, feedback, state):
        feedback.values = {"tournament_id": state.active_tournament, "name": None}
        saved_dict = state.new_round
        self.load_values(feedback, saved_dict)
        if (state.validation and feedback.raw_values == ['']) or state.prediction or feedback.parsed:
                return None
        else:
            state.default_command = "new_round"
            state.next_key = feedback.errors[-1]
            state.new_round = {key: value for key, value in feedback.values.items() if value is not None}
            return None


    def execute(self, feedback, db, state):
        table = db.table("tournaments")
        stringified_tournament = table.get(doc_id=feedback.values["tournament_id"])
        if stringified_tournament is None or "matches" not in state.new_round.keys():
            feedback.title = f"Nouvelle Ronde : Echec!"
            if stringified_tournament is None:
                feedback.data = [f"Le tournoi {feedback.values['tournament_id']} n'existe pas!"]
            else:
                feedback.data = ["La ronde précédente n'est pas terminée!"]
            state.default_command = None
            state.next_key = None
            state.new_round = {}
            return None
        tournament = Tournament(db, **stringified_tournament)
        round = Round(name=feedback.values["name"], tournament=tournament.id)
        round.add_matches(*state.new_round["matches"])
        tournament.new_round(round)
        tournament.complete_update(db)
        state.default_command = "update_round"
        state.next_key = "player_id"
        state.last_command = "new_round"
        if state.active_tournament != tournament.id:
            state.active_tournament = tournament.id
            feedback.info = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
        feedback.title = "Nouvelle ronde démarrée:"
        feedback.data = [round]
        state.new_round = {}
        return None