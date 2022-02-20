from reports.list_tournament_players import ListTournamentPlayers

class ListTournamentRanks(ListTournamentPlayers):
    def __init__(self):
        self.commands = ("ltc", "ltk")
        self.natural = [["liste", "tournoi", "classements", "list", "tournament", "ranks"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        new_dict, errors = super().parse_values(raw_values, state)
        state.default_command = "list_tournament_ranks"
        return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        feedback["title"] = feedback["title"].split(',')[0] + ", Classements"
        feedback["data"] = feedback["data"].sort(key=lambda player: player.ranking)
        return feedback