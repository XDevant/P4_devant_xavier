from tinydb import where
from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament

class Report(Command):
    def __init__(self):
        self.commands = (".lt", ".lj", ".lp", ".lc", ".lk", ".ltj", ".ltp", ".ltc", ".ltk", ".ltr", ".ltm")
        self.natural = [["list", "joueur", "player", "classement", "ranking"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if 't' not in raw_command or raw_command[-1] == 't':
            return True, {}
        else:
            check = False
            values = {'id': -1}
            if raw_values is not None:
                value = raw_values[0].split('=')[-1].strip()
                if value.isnumeric():
                    values['id'] = int(value)
                    return int(value) > 0, values
            if state.default_tournament is not None:
                values['id'] = state.default_tournament
                return True, values
            else:
                return False, values


    def execute(self, raw_command, values, db, state):
        match raw_command:
            case ".lt":
                table = db.table("tournaments")
                tournaments = sorted(table.all(), key=lambda tournament: tournament['date'])
                name = "Rapport: Liste des Tournois"
                return name, [Tournament(db, **tournament) for tournament in tournaments]
            case ".lj" | ".lp":
                table = db.table("players")
                players = sorted(table.all(), key=lambda player: player['last_name'] + player['first_name'])
                name = "Rapport: Liste des Joueurs (alphabétique)"
                return name, [Player(**player) for player in players]
            case ".lc" | ".lk":
                table = db.table("players")
                players = sorted(table.all(), key=lambda player: player['ranking'])
                name = "Rapport: Liste des Joueurs (classement)"
                return name, [Player(**player) for player in players]
            case ".ltc" | ".ltk" | ".ltj" | ".ltp":
                tournament = Tournament(db, **db.table("tournaments").get(doc_id=values['id']))
                name = f"Rapport: Liste des Joueurs, Tournoi {tournament.name} (n°{values['id']})"
                player_ids = tournament.players
                if player_ids == []:
                    return name, ["Aucun joueur inscrit en tournoi"]
                table = db.table("players")
                players = []
                for id in player_ids:
                    players.append(table.get(doc_id=id))
                print(players)
                if raw_command in [".ltc", ".ltk"]:
                    players.sort(key=lambda player: player['ranking'])
                    name += " (classement)"
                else:
                    print("b")
                    players.sort(key=lambda player: player['last_name'] + player['first_name'])
                    name += " (alphabétique)"
                return name, [Player(**player) for player in players]
            case ".ltr":
                tournament = Tournament(db, **db.table("tournaments").get(doc_id=values['id']))
                rounds = [round.name for round in tournament.round_details]
                name = f"Rapport: Liste des Rondes, Tournoi {tournament.name} (n°{values['id']})"
                return name, rounds
            case ".ltm":
                tournament = Tournament(db, **db.table("tournaments").get(doc_id=values['id']))
                matchs = tournament.round_details
                name = f"Rapport: Liste des Matches, Tournoi {tournament.name} (n°{values['id']})"
                return name, matchs