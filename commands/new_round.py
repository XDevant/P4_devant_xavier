from datetime import datetime
from commands.command import Command
from db_models.tournament import Tournament
from db_models.round import Round


class NewRound(Command):
    def __init__(self):
        self.commands = (".rd", ".rs")
        self.natural = [["ronde", "démarrer", "round" "start"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is not None:
            values = {"name": raw_values[0].split('=')[-1]}
            if len(values["name"]) > 0:
                return True, values
        return True, {"name": state.round_in_process["name"]}

    def execute(self, raw_command, values, db, state):
        round = Round(name=values["name"])
        round.add_matches(*state.round_in_process["matches"])
        table = db.table("tournaments")
        tournament = Tournament(db, **table.get(doc_id=state.default_tournament))
        tournament.new_round(round)
        round.register(db.table("rounds"))
        tournament.complete_update(db)
        print(round)
        return "Nouvelle ronde démarrée:", [round]