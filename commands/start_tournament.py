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


    def parse_values(self, raw_values, state):
        if state.validation:
            dict = {"tournament_id": None}
            saved_dict = {"tournament_id": state.default_tournament}
        else:
            dict = {"tournament_id": state.default_tournament}
            saved_dict = {}
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if (state.validation and raw_values == ['']) or state.prediction:
                return new_dict, [[]]
        if state.validation:
            state.validation = False
            errors = ["Commande annulée Tournoi non démarré"]
            state.default_command = "update_tournament"
            state.next_key = None
            return new_dict, errors
        if check:
            return new_dict, errors
        else:
            state.default_command = "start_tournament"
            state.next_key = errors[-1]
        return new_dict, errors


    def execute(self, values, db, state):
        feedback = super().execute( values, db, state)
        table = db.table("tournaments")
        tournament = Tournament(db, **table.get(doc_id=values["tournament_id"]))
        count = len(tournament.players)
        if tournament.round == 0:
            if count % 2 != 0 or count <= tournament.rounds:
                feedback["title"] = "Nombre d'inscrits impair ou  insuffisant!"
                state.default_command = "update_tournament"
        elif tournament.round_details[-1].chech_matches() >= 0:
            feedback["title"] = "Nouvelle Ronde: Echec! La ronde actuelle n'est pas terminée!"
            state.default_command = "update_tournament"
        elif tournament.finished:
            feedback["title"] = "Tournoi déja terminé"
            state.default_command = None
        elif not tournament.registered:
            feedback["title"] =  "Tournoi non enregistré"
            state.default_command = "new_tournament"
        elif state.validation:
            if tournament.round == 0:
                feedback["title"] = "Tournoi démarré:"
                tournament.started = True
                state.default_tournament = None
            else:
                feedback["title"] = "Nouveau Round démarré:"
                tournament.round_details[-1].validate()
            round = Round(name=f"Round {tournament.round + 1}", tournament=tournament.id)
            round.add_matches(*self.generate_round(tournament, db, state))
            tournament.new_round(round)
            tournament.complete_update(db)
            feedback["data"] = [tournament]

            state.default_command = "update_round"
            state.next_key = "player_id"
            state.active_tournament = tournament.id
            state.last_command = "start_tournament"
            state.validation = False
            feedback["info"] = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
            return feedback
        else:
            if tournament.round == 0:
                feedback["title"] = f"Veillez confirmer la commande Démarrer Tournoi n°{tournament.id}.(Entrée)"
            else:
                feedback["title"] = f"Veillez confirmer la commande Démarrer nouveau Round n°{tournament.id}.(Entrée)"
            feedback["data"] = [tournament]
            feedback["info"] = "Vous pouver saisir n'importe quel autre caractère pour annuler."
            state.validation = True
            state.default_command = "start_tournament"
            state.default_tournament = tournament.id
        state.next_key = None
        return feedback

    
    def generate_round(self, tournament, db, state):
        active_tournament = TournamentSprite(tournament, db)
        matches = active_tournament.generate_matches()
        return matches
