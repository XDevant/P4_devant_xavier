from commands.command import Command
from models.round import Round
from controlers.sprite import TournamentSprite


class StartTournament(Command):
    def __init__(self):
        self.commands = ["td", "ts", "dt", "st", "dr", "sr", "rd", "rs", "tt"]
        self.keys = ["tournament_id"]
        self.values = [None]
        self.next_command = "update_round"
        self.previous_command = "update_tournament"

    def is_the_one(self, input):
        return super().is_the_one(input)

    def parse_values(self, feedback, state):
        if state.active_tournament is None:
            default = state.default_tournament
        else:
            default = state.active_tournament
        if state.validation:
            feedback.values = {"tournament_id": None}
            saved_dict = {"tournament_id": default}
        else:
            feedback.values = {"tournament_id": default}
            saved_dict = {}
        if state.validation and feedback.raw_values != ['']:
            state.validation_failure(feedback)
            state.default_command = None
            feedback.title = "Démarrer tournoi/Nouveau Round :"
            feedback.data = ["Commande annulée"]
            return None
        self.load_values(feedback, saved_dict)
        if state.validation or state.prediction or feedback.parsed:
            feedback.parsed = True
            if state.validation:
                feedback.success = True
        else:
            state.parsing_failure(feedback)
        return None

    def execute(self, feedback, db, state):
        feedback.title = "Démarrer Tournoi/Nouveau Round:"
        tournament = self.load_tournament(feedback, db, state)
        if tournament is None:
            state.clear_menu()
            return None
        info = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
        check_1 = self.check_start(feedback, state, tournament)
        check_2 = self.check_end_round(feedback, state, tournament)
        check_3 = self.check_ended(feedback, state, tournament)
        if not(check_1 and check_2 and check_3):
            state.clear_menu()
            return None
        if state.validation:
            if tournament.round == tournament.rounds:
                feedback.title = "Tournoi terminé:"
                tournament.finished = True
                tournament.round_details[-1].validate()
                state.active_tournament = None
                state.validation = False
                state.clear_menu()
            else:
                if tournament.round == 0:
                    feedback.title = "Tournoi démarré:"
                    tournament.started = True
                    state.default_tournament = None
                else:
                    feedback.title = "Nouveau Round démarré:"
                    tournament.round_details[-1].validate()
                round = Round(name=f"Round {tournament.round + 1}", tournament=tournament.id)
                matches = self.generate_round(tournament, db)
                print(matches)
                round.add_matches(*matches)
                round.register(db)
                tournament.new_round(round)
                feedback.info = info
                state.start_ok(feedback, tournament.id, self.next_command)
            tournament.complete_update(db)
            feedback.data = [tournament.round_details[-1]]
        else:
            feedback.title = "Veillez confirmer la commande "
            if tournament.round == 0:
                feedback.title += f"Démarrer Tournoi n°{tournament.id}.(Entrée)"
            elif tournament.round == tournament.rounds:
                feedback.title += f"Terminer Tournoi n°{tournament.id}.(Entrée)"
            else:
                feedback.title += f"Démarrer Round n°{tournament.round + 1}.(Entrée)"
            feedback.info = "Vous pouver saisir n'importe quel autre caractère pour annuler."
            feedback.data = [tournament]
            state.validation_started(feedback)
            state.default_tournament = tournament.id
        return None

    def generate_round(self, tournament, db):
        active_tournament = TournamentSprite(tournament, db)
        matches = active_tournament.generate_matches()
        return matches
