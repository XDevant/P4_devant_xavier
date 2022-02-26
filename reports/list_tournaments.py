from commands.command import Command
from models.tournament import Tournament


class ListTournaments(Command):
    def __init__(self):
        self.commands = ["lt"]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.parsed = True
        return None

    def execute(self, feedback, db, state):
        table = db.table("tournaments")
        tournaments = sorted(table.all(), key=lambda tournament: tournament['date'])
        feedback.title = "Rapport: Liste des Tournois"
        feedback.data = [Tournament(db, **tournament) for tournament in tournaments]
        feedback.succes = True
        state.last_command = feedback.command
        return None
