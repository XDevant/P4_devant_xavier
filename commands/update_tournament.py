from commands.command import Command
from db_models.tournament import Tournament



class UpdateTournament(Command):
    def __init__(self):
        self.commands = ("mt", "tm", "tu", "ut")
        self.natural = [["tournoi", "actualiser", "tournament", "update"]]


    def is_the_one(self, input):
        return super().is_the_one(input)


    def parse_values(self, raw_values, state):
        dict = {"tournament_id": state.default_tournament, "player_id": state.default_player}
        saved_dict = state.update_tournament
        check, new_dict, errors = self.load_values(raw_values, dict, saved_dict)
        if check:
            return new_dict, errors
        else:
            state.default_command = "update_tournament"
            state.next_key = errors[-1]
            state.update_tournament = {key: value for key, value in new_dict.items() if value is not None}
            return new_dict, errors


    def execute(self, values, db, state):
        table = db.table("tournaments")
        tournament = table.get(doc_id=values['tournament_id'])
        new_item = Tournament(db, **tournament)
        validation = new_item.add_player(values["player_id"])
        if not validation:
            return "Joueur déjà inscrit", []
        new_item.complete_update(db)

        state.default_tournament = new_item.id
        state.update_tournament = {}
        state.default_command = None
        state.last_command = "update_tournament"
        state.next_key = None

        feedback = super().execute( values, db, state)
        feedback["name"] = "Nouveau joueur inscrit:"
        feedback["data"] = [new_item]
        return feedback
