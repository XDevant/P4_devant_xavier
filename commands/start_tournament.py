from commands.command import Command
from db_models.tournament import Tournament


class StartTournament(Command):
    def __init__(self):
        self.commands = (".td", ".ts")
        self.natural = [["tournoi", "démarrer", "tournament" "start"]]
        self.values = True
        self.next_command = ".rd"

    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None and state.default_tournament is None:
            return False, {}
        elif raw_values is not None:
            values = {"id": int(raw_values[0].split('=')[-1])}
            if values["id"] > 0:
                return True, values
        return True, state.default_tournament


    def execute(self, raw_command, values, db, state):
        name = "Tournoi démarré:"
        table = db.table("tournaments")
        tournament = Tournament(db, **table.get(doc_id=values["id"]))
        if len(tournament.players) % 2 != 0:
            return "Nombre d'inscrits impair !", []
        elif len(tournament.players) <= tournament.rounds:
            return "Nombre d'inscrits insuffisant !", []
        elif tournament.finished:
            return "Tournoi déja terminé", []
        elif not tournament.registered:
            return "Tournoi non enregistré", []
        else:
            tournament.started = True
            tournament.complete_update(db)
            return name, [tournament]


class CertifyRound(StartTournament):
    def __init__(self):
        self.commands = (".rv", ".rc")
        self.natural = [["ronde", "valider", "round" "certify"]]
        self.values = True
        self.next_command = ".rd"


    def execute(self, raw_command, values, db, state):
        name = "Ronde validée:"
        table = db.table("tournaments")
        tournament = Tournament(**table.get(doc_id=values["id"]))
        if True:
            return name, [tournament]
        else:
            return "Résultats manquants:", []