from commands.command import Command


class UpdateRound(Command):
    def __init__(self):
        self.commands = ["mr", "rm", "ru", "ur"]
        self.keys = ["tournament_id", "player_id", "score"]
        self.values = [None, None, None]

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        feedback.values = {key: value for key, value in zip(self.keys, self.values)}
        feedback.values["tournament_id"] = state.active_tournament
        saved_dict = state.update_round
        self.load_values(feedback, saved_dict)
        if state.prediction or feedback.parsed:
            return None
        else:
            state.parsing_failure(feedback)
            return None

    def execute(self, feedback, db, state):
        feedback.title = "Nouveau résultat: Echec"
        tournament_id = feedback.values['tournament_id']
        tournament = self.load_tournament(feedback, db, state)
        if tournament is None:
            state.execute_refused(feedback, tournament_id == state.default_tournament)
            return None
        if len(tournament.round_details) == 0:
            feedback.important = f"Le tournoi {tournament_id} n'est pas démarré!"
            state.execute_refused(feedback, False)
            return None
        round = tournament.round_details[-1]
        i, j = round.find_indexes(feedback.values["player_id"])
        if i < 0:
            state.execute_refused(feedback, False)
            feedback.important = f"Joueur {i} non inscrit"
            return None
        if j == 0:
            points_a = feedback.values["score"]
            if round.matches[i][1][1] is None:
                points_b = 1 - feedback.values["score"]
            else:
                points_b = round.matches[i][1][1]
        else:
            points_b = feedback.values["score"]
            if round.matches[i][0][1] is None:
                points_a = 1 - feedback.values["score"]
            else:
                points_a = round.matches[i][0][1]
        round.update_match(i, points_a, points_b)
        tournament.round_details[-1] = round
        tournament.complete_update(db)
        if round.chech_matches() == -1:
            feedback.important = f"Le round n°{tournament.round} est complet"
            if tournament.round == tournament.rounds:
                feedback.important += ", entrez .tt pour clore le Tournoi."
            else:
                feedback.important += ", entrez .dr pour commencer un nouveau round."
        state.execute_succes(feedback)
        state.next_keys = ["player_id"]
        if state.active_tournament != tournament.id:
            state.active_tournament = tournament.id
            feedback.info = f"Le tournoi n°{tournament.id} est le tournoi actif par default."

        feedback.title = "Nouveau résultat:"
        feedback.data = [tournament]
        return None
