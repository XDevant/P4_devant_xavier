from commands.command import Command
from db_models.tournament import Tournament
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
        if (state.validation and raw_values == []) or state.prediction:
                return new_dict, [[]]
        if state.validation:
            state.validation = False
            errors = ["Commande annulée Tournoi non démarré"]
            state.default_command = "update_tournament"
            state.next_key = None
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
        if count % 2 != 0 or count <= tournament.rounds:
            feedback["title"] = "Nombre d'inscrits impair ou  insuffisant!"
            state.default_command = "update_tournament"
        elif tournament.finished:
            feedback["title"] = "Tournoi déja terminé"
            state.default_command = None
        elif not tournament.registered:
            feedback["title"] =  "Tournoi non enregistré"
            state.default_command = "new_tournament"
        elif state.validation:
            feedback["title"] = "Tournoi démarré:"
            tournament.started = True
            tournament.complete_update(db)
            feedback["data"] = [tournament]
            self.new_round(tournament, db, state)

            state.default_command = "new_round"
            state.next_key = "name"
            state.default_tournament = None
            state.active_tournament = tournament.id
            state.last_command = "start_tournament"
            state.validation = False
            feedback["info"] = f"Le tournoi n°{tournament.id} est le tournoi actif par default."
            return feedback
        else:
            feedback["title"] = f"Veillez confirmer la commande Démarrer Tournoi n°{tournament.id}.(Entrée)"
            feedback["data"] = [tournament]
            feedback["info"] = "Vous pouver saisir n'importe quel autre caractère pour annuler."
            state.validation = True
            state.default_command = "start_tournament"
            state.default_tournament = tournament.id
        state.next_key = None
        return feedback

    
    def new_round(self, tournament, db, state):
        active_tournament = TournamentSprite(tournament, db)
        matches = active_tournament.generate_matches()
        state.new_round['name'] = f"Round {active_tournament.round + 1}"
        state.new_round['matches'] = matches


class CertifyRound(StartTournament):
    def __init__(self):
        self.commands = (".rv", ".rc")
        self.natural = [["ronde", "valider", "round" "certify"]]
        self.next_command = ".rd"


    def execute(self, values, db, state):
        table = db.table("tournaments")
        tournament = Tournament(db, **table.get(doc_id=values["tournament_id"]))
        check = tournament.round_details[-1].validate()
        if check:
            name = "Ronde validée: "
            tournament.complete_update(db)
            self.new_round(tournament, db, state)
            data = [tournament]
        else:
            name = "Résultats manquants:"
            data = []
        return name, data