from commands.command import Command
from models.tournament import Tournament



class UpdateTournament(Command):
    def __init__(self):
        self.commands = ("mt", "tm", "tu", "ut")
        self.natural = [["tournoi", "actualiser", "tournament", "update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        if state.validation:
            dict = {"tournament_id": None, "player_id": None}
        else:
            dict = {"tournament_id": state.default_tournament, "player_id": state.default_player}
        saved_dict = state.update_tournament
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        state.update_tournament = {key: value for key, value in new_dict.items() if value is not None}
        if (state.validation and raw_values == ['']) or state.prediction:
            return new_dict, [[]]
        if state.validation:
            state.validation = False
            errors = ["Commande annulée Joueur toujours inscrit"]
            state.default_command = "update_tournament"
            state.update_tournament = {}
            return new_dict, errors
        if check:
            return new_dict, errors
        else:
            state.default_command = "update_tournament"
            state.next_key = errors[-1]
            return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        feedback["title"] = f"Tournoi n°{values['tournament_id']}, inscription nouveau Joueur {values['player_id']}:"
        table = db.table("tournaments")
        stringified_tournament = table.get(doc_id=values['tournament_id'])
        failure = False
        if stringified_tournament is None:
            feedback["data"] = ["Le tournoi n'existe pas!"]
            failure = True
        tournament = Tournament(db, **stringified_tournament)
        if tournament.started:
            feedback["data"] = ["Le tournoi est déja commencé"]
            failure = True
        if failure:
            state.update_tournament = {}
            state.next_key = None
            if values['tournament_id'] == state.default_tournament:
                state.default_tournament = None
            return feedback

        player = tournament.add_player(values['player_id'])
        if player == -1 and not state.validation:
            feedback["title"] = f"Tournoi n°{tournament.id}, Veillez confirmer la commande Désinscrire Joueur.(Entrée)"
            feedback["data"] = [f"Joueur {values['player_id']} inscrit"]
            state.validation = True
            feedback["info"] = "Vous pouver saisir n'importe quel autre caractère pour annuler."
        else:
            if state.validation:
                state.validation = False
                tournament.remove_player(values['player_id'])
                feedback["title"] = f"Tournoi n°{tournament.id}, Joueur {values['player_id']} désinscrit:"
            state.update_tournament = {}
            tournament.complete_update(db)
            feedback["data"] = [tournament]
        state.next_key = "player_id"
        state.last_command = "update_tournament"
        if tournament.id != state.default_tournament:
            state.default_tournament = tournament.id
            feedback["info"] = f"Le tournoi {tournament.id} est maintenant le tournoi par défaut."
        state.default_command = "update_tournament"
        return feedback
