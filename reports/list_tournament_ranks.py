from reports.list_tournament_players import ListTournamentPlayers


class ListTournamentRanks(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltc", "ltk")
        self.natural = [["liste", "tournoi", "classements", "list", "tournament", "ranks"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        super().parse_values(feedback.raw_values, state)
        state.default_command = "list_tournament_ranks"
        return None


    def execute(self, feedback, db, state):
        super().execute(feedback, db, state)
        feedback.title = feedback.title.split(',')[0] + ", Classements"
        if not isinstance(feedback.data[0], str):
            feedback.data.sort(key=lambda player: player.ranking)
        return None