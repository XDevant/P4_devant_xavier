from commands.command import Command
from models.tournament import Tournament



class UpdateTournament(Command):
    def __init__(self):
        self.commands = ("mt", "tm", "tu", "ut")
        self.natural = [["tournoi", "actualiser", "tournament", "update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, feedback, state):
        if state.validation:
            feedback.values = {"tournament_id": None, "player_id": None}
        else:
            feedback.values = {"tournament_id": state.default_tournament, "player_id": None}
        saved_dict = state.update_tournament
        self.load_values(feedback, saved_dict)
        state.update_tournament = {key: value for key, value in feedback.values.items() if value is not None}
        if (state.validation and feedback.raw_values == ['']) or state.prediction or feedback.parsed:
            return None
        if state.validation:
            state.validation_failure(feedback)
            feedback.errors = ["Commande annulée Joueur toujours inscrit"]
        else:
            state.parsing_failure(feedback)
        return None


    def execute(self, feedback, db, state):
        tournament_id = feedback.values['tournament_id']
        player_id = feedback.values['player_id']
        feedback.title = f"Tournoi n°{tournament_id}, inscription nouveau Joueur {player_id}:"
        table = db.table("tournaments")
        stringified_tournament = table.get(doc_id=tournament_id)
        if stringified_tournament is None:
            feedback.data = ["Le tournoi {tournament_id} n'existe pas!"]
            state.execute_refused(feedback, tournament_id == state.default_tournament)
            return None
        tournament = Tournament(db, **stringified_tournament)
        if tournament.started:
            feedback.data = ["Le tournoi {tournament_id} est déja commencé"]
            state.execute_refused(feedback, tournament_id == state.default_tournament)
            return None
        stringified_player = table.get(doc_id=player_id)
        if stringified_player is None:
            feedback.data = ["Le jouer {player_id} n'existe pas!"]
            state.execute_refused(feedback, False)
            return None
        player = tournament.add_player(player_id)
        if player == -1 and not state.validation:
            state.validation = True
            feedback.title = f"Tournoi n°{tournament_id}, Veillez confirmer la commande Désinscrire Joueur.(Entrée)"
            feedback.data = [f"Joueur {player_id} déjà inscrit"]
            feedback.info = "Vous pouver saisir n'importe quel autre caractère pour annuler."
        else:
            if state.validation:
                state.validation = False
                tournament.remove_player(player_id)
                feedback.title = f"Tournoi n°{tournament_id}, Joueur {player_id} désinscrit:"
            state.update_tournament = {}
            tournament.complete_update(db)
            feedback.data = [tournament]
        state.next_key = "player_id"
        state.last_command = "update_tournament"
        if tournament_id != state.default_tournament:
            state.default_tournament = tournament_id
            feedback.info = f"Le tournoi {tournament_id} est maintenant le tournoi par défaut."
        state.default_command = "update_tournament"
        return None
