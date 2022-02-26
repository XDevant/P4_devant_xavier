from reports.list_tournament_players import ListTournamentPlayers


class ListTournamentRanks(ListTournamentPlayers):
    def __init__(self):
        self.commands = ["ltc", "ltk"]

    def is_the_one(self, input):
        if input in self.commands:
            return True
        return False

    def parse_values(self, feedback, state):
        super().parse_values(feedback, state)
        state.default_command = "list_tournament_ranks"
        return None

    def execute(self, feedback, db, state):
        super().execute(feedback, db, state)
        feedback.title = feedback.title.split(',')[0] + ", Classements"
        if not isinstance(feedback.data[0], str):
            feedback.data.sort(key=lambda player: player.ranking)
        feedback.succes = True
        return None
