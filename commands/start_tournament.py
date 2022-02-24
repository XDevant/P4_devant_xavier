from commands.command import Command
from models.tournament import Tournament
from models.round import Round
from controlers.sprite import TournamentSprite


class StartTournament(Command):
    def __init__(self):
        self.commands = ["td", "ts", "dt", "st", "dr", "sr", "rd", "rs"]
        self.natural = [["tournoi", "démarrer", "tournament" "start"]]

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
            feedback.title = f"Démarrer tournoi/Nouveau Round :"
            feedback.data = ["Commande annulée"]
            return None

        self.load_values(feedback, saved_dict)
        if state.validation  or state.prediction or feedback.parsed:
            feedback.parsed = True
            if state.validation:
                feedback.success = True
        else:
            state.parsing_failure(feedback)
        return None


    def execute(self, feedback, db, state):
        feedback.title = "Démarrer Tournoi/Nouveau Round:"
        table = db.table("tournaments")
        stringified_tournament = table.get(doc_id=feedback.values["tournament_id"])
        if stringified_tournament is None:
            feedback.important = f"Le tournoi {feedback.values['tournament_id']} n'existe pas!"
            state.default_command = None
            return None
        tournament = Tournament(db, **stringified_tournament)
        if tournament.round == 0 and (len(tournament.players) % 2 != 0 or len(tournament.players) <= tournament.rounds):
                feedback.title = "Démarrer Tournoi:"
                feedback.important = "Nombre d'inscrits impair ou insuffisant!"
                state.default_command = "update_tournament"
                state.default_tournament = tournament.id
        elif tournament.round > 0 and tournament.round_details[-1].chech_matches() >= 0:
            feedback.title = "Démarrer Nouveau Round:"
            feedback.important = "Echec! La ronde actuelle n'est pas terminée!"
            state.default_command = "update_tournament"
            state.active_tournament = tournament.id
        elif tournament.finished:
            feedback.title = "Démarrer Nouveau Round:"
            feedback.important = "Tournoi déja terminé"
            state.default_command = None
            state.active_tournament = None
        elif state.validation:
            if tournament.round == 0:
                feedback.title = "Tournoi démarré:"
                tournament.started = True
                state.default_tournament = None
            else:
                feedback.title = "Nouveau Round démarré:"
                tournament.round_details[-1].validate()
            round = Round(name=f"Round {tournament.round + 1}", tournament=tournament.id)
            round.add_matches(*self.generate_round(tournament, db, state))
            round.register(db)
            tournament.new_round(round)
            tournament.complete_update(db)
            feedback.data = [tournament]

            state.default_command = "update_round"
            state.next_key = "player_id"
            state.active_tournament = tournament.id
            state.last_command = "start_tournament"
            state.validation = False
            feedback.info = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
            return None
        else:
            if tournament.round == 0:
                feedback.title = f"Veillez confirmer la commande Démarrer Tournoi n°{tournament.id}.(Entrée)"
            else:
                feedback.title = f"Veillez confirmer la commande Démarrer nouveau Round n°{tournament.id}.(Entrée)"
            feedback.data = [tournament]
            feedback.info = "Vous pouver saisir n'importe quel autre caractère pour annuler."
            state.validation = True
            state.default_command = feedback.command
            state.default_tournament = tournament.id
            feedback.success = True
        state.next_key = None
        return None

    
    def generate_round(self, tournament, db, state):
        active_tournament = TournamentSprite(tournament, db)
        matches = active_tournament.generate_matches()
        return matches
