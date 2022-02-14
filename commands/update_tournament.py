from commands.command import Command
from db_models.tournament import Tournament



class UpdateTournament(Command):
    def __init__(self):
        self.commands = (".ta", ".tu")
        self.natural = [["tournoi", "actualiser", "tournament", "update"]]
        self.values = {"tournament_id": None, "player_id": None}


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_command, raw_values, state):
        if raw_values is None:
            return False, {}
        new_dict = self.values
        saved_dict = state.tournament_update_in_process
        return self.load_values(raw_values, new_dict, saved_dict)


    def check_value(self, key, value):
        return int(value) > 0


    def execute(self, raw_command, values, db, state):
        name = "Nouveau joueur inscrit:"
        table = db.table("tournaments")
        tournament = table.get(doc_id=values['tournament_id'])
        new_item = Tournament(db, **tournament)
        validation = new_item.add_player(values["player_id"])
        if not validation:
            return "Joueur déjà inscrit", []
        new_item.complete_update(db)
        return name, [new_item]
