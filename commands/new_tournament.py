from commands.command import Command
from models.tournament import Tournament


class NewTournament(Command):
    def __init__(self):
        self.commands = ["nt", "tn"]
        self.natural = [["nouveau", "new"], ["tournoi", "tournament"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.values = {"name": None, "place": None, "date": None, "description": None, "rule": None, "rounds": 4}
        saved_dict = state.new_tournament
        self.load_values(feedback, saved_dict)
        if feedback.parsed:
            return None
        else:
            state.parsing_failure(feedback)
            return None


    def execute(self, feedback, db, state):
        tournament = Tournament(db, **feedback.values)
        tournament.register(db)
        
        state.execute_succes(feedback)
        state.default_tournament = tournament.id
        state.default_command = "update_tournament"

        feedback.title = "Nouveau Tournoi crée:"  
        feedback.data = [tournament]
        feedback.info = f"Le tournoi {tournament.id} est maintenant le tournoi par défaut."
        return None