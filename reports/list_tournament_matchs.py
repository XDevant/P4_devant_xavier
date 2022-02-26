from reports.list_tournament_players import ListTournamentPlayers


class ListTournamentMatchs(ListTournamentPlayers):
    def __init__(self):
        self.commands = ["ltm"]

    def is_the_one(self, input):
        if input in self.commands:
            return True
        return False

    def parse_values(self, feedback, state):
        super().parse_values(feedback, state)
        state.default_command = feedback.command
        return None

    def execute(self, feedback, db, state):
        feedback.title = "Rapport: Tournoi, Liste des Matches"
        tournament = self.load_tournament(feedback, db, state)
        if tournament is None:
            feedback.data = ["Aucun tournoi correspondant à cet identifiant"]
        else:
            new_title = f" {tournament.name} (n°{tournament.id}),"
            splited_title = feedback.title.split(',')
            feedback.title = splited_title[0] + new_title + splited_title[0]
            rounds = tournament.round_details
            if len(rounds) > 0:
                feedback.data = rounds
            else:
                feedback.data = ["Aucun round trouvé pour ce tournoi"]
            feedback.succes = True
        state.default_command = None
        state.next_key = None
        return None
