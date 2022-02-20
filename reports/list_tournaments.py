from commands.command import Command
from db_models.tournament import Tournament


class ListTournaments(Command):
    def __init__(self):
        self.commands = ("lt")
        self.natural = [["liste", "tournois", "list", "tournaments"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        return super().parse_values(raw_values, state)


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        table = db.table("tournaments")
        tournaments = sorted(table.all(), key=lambda tournament: tournament['date'])
        feedback["title"] = "Rapport: Liste des Tournois"
        feedback["data"] = [Tournament(db, **tournament) for tournament in tournaments]
        return feedback