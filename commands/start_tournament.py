from commands.command import Command
from models.tournament import Tournament
from models.round import Round
from controlers.sprite import TournamentSprite


class StartTournament(Command):
    def __init__(self):
        self.commands = ("td", "ts", "dt", "st")
        self.natural = [["tournoi", "démarrer", "tournament" "start"]]
        self.next_command = ".rd"

    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        if state.validation:
            feedback.values = {"tournament_id": None}
            saved_dict = {"tournament_id": state.default_tournament}
        else:
            feedback.values = {"tournament_id": state.default_tournament}
            saved_dict = {}
        self.load_values(feedback, saved_dict)
        if (state.validation and feedback.raw_values == ['']) or state.prediction or feedback.parsed:
                return None
        if state.validation:
            state.validation = False
            feedback.errors = ["Commande annulée Tournoi non démarré"]
            state.default_command = "update_tournament"
            state.next_key = None
            return None
        else:
            state.default_command = "start_tournament"
            state.next_key = feedback.errors[-1]
        return None


    def execute(self, feedback, db, state):
        table = db.table("tournaments")
        tournament = Tournament(db, **table.get(doc_id=feedback.values["tournament_id"]))
        count = len(tournament.players)
        if tournament.round == 0:
            if count % 2 != 0 or count <= tournament.rounds:
                feedback.title = "Nombre d'inscrits impair ou  insuffisant!"
                state.default_command = "update_tournament"
        elif tournament.round_details[-1].chech_matches() >= 0:
            feedback.title = "Nouvelle Ronde: Echec! La ronde actuelle n'est pas terminée!"
            state.default_command = "update_tournament"
        elif tournament.finished:
            feedback.title = "Tournoi déja terminé"
            state.default_command = None
        elif not tournament.registered:
            feedback.title =  "Tournoi non enregistré"
            state.default_command = "new_tournament"
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
        state.next_key = None
        return None

    
    def generate_round(self, tournament, db, state):
        active_tournament = TournamentSprite(tournament, db)
        matches = active_tournament.generate_matches()
        return matches
