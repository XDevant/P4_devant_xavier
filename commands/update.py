from commands.command import Command
from db_models.player import Player
from db_models.tournament import Tournament



class Update(Command):
    def __init__(self):
        self.commands = (".ja", ".ta", ".pu", ".tu")
        self.natural = [["joueur", "tournoi", "ronde", "actualiser" "player", "tournament", "round", "update"]]
        self.values = True


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        if 't' in raw_command:
            new_dict = {"tournament_id": None, "player_id": None,}
            saved_dict = state.tournament_update_in_process
        else:
            new_dict = {"player_id": None, "ranking": None,}
            saved_dict = state.player_update_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        return int(value) > 0


    def execute(self, raw_command, values, db, state):
        if 't' in raw_command:
            name = "Nouveau joueur inscrit:"
            table = db.table("tournaments")
            tournament = table.get(doc_id=values['tournament_id'])
            new_item = Tournament(**tournament)
            validation = new_item.add_player(values["player_id"])
            if not validation:
                return "Joueur déjà inscrit", []
        else:
            name = "Nouveau classement:"
            table = db.table("players")
            new_item = Player(**table.get(doc_id=values['player_id']))
            new_item.ranking = values["ranking"]
        new_item.complete_update(table)
        return name, [new_item]
