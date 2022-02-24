from commands.command import Command
from models.player import Player
from models.tournament import Tournament



class UpdateRound(Command):
    def __init__(self):
        self.commands = ["mr", "rm", "ru", "ur"]
        self.natural = [["ronde", "actualiser", "round", "update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        feedback.values = {"tournament_id": state.active_tournament, "player_id": None, "score": None}
        saved_dict = state.update_round
        self.load_values(feedback, saved_dict)
        if state.prediction or feedback.parsed:
            return None
        else:
            state.parsing_failure(feedback)
            return None
    

    def execute(self, feedback, db, state):
        table = db.table("tournaments")
        print(feedback.values)
        tournament_id = feedback.values['tournament_id']
        stringified_tournament = table.get(doc_id=tournament_id)
        if stringified_tournament is None:
            feedback.important = f"Le tournoi {tournament_id} n'existe pas!"
            state.execute_refused(feedback, tournament_id == state.default_tournament)
            return None
        print(stringified_tournament)
        tournament = Tournament(db, **stringified_tournament)
        print("tournoi")
        print(tournament.id)
        if len(tournament.round_details) == 0:
            feedback.important = f"Le tournoi {tournament_id} n'est pas démarré!"
            state.execute_refused(feedback, False)
            return None
        round = tournament.round_details[-1]
        i, j = round.find_indexes(feedback.values["player_id"])
        if i < 0:
            state.execute_refused(feedback, False)
            feedback.title = "Nouveau résultat: Echech"
            feedback.important = f"Joueur {i} non inscrit"
            return feedback
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
            feedback.important = f"Le round n°{tournament.round} est complet, entrez .dr pour commencer un nouveau round."
        state.execute_succes(feedback)
        state.next_keys = ["player_id"]
        if state.active_tournament != tournament.id:
            state.active_tournament = tournament.id
            feedback.info = f"Le tournoi n°{tournament.id} est le tournoi actif par default."

        feedback.title = "Nouveau résultat:"
        feedback.data = [tournament]
        return None
