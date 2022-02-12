import json
from tinydb.table import Document
from datetime import date
from db_models.round import Round


class Tournament:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name =  kwargs['name']
        else:
            self.name = None
        if 'place' in kwargs:
            self.place =  kwargs['place']
        else:
            self.place = None
        if 'date' in kwargs:
            self.date =  kwargs['date']
        else:
            self.date = str(date.today())
        if 'description' in kwargs:
            self.description =  kwargs['description']
        else:
            self.description = 'No Description'
        if 'rounds' in kwargs:
            self.rounds =  kwargs['rounds']
        else:
            self.rounds = 4
        if 'timer' in kwargs:
            self.timer =  kwargs['timer']
        else:
            self.timer = 'blitz'
        if 'round_details' in kwargs:
            self.round_details = [Round(**round_dict) for round_dict in kwargs['round_details']] # need chk
        else:
            self.round_details = []
        if 'players' in kwargs:
            self.players =  kwargs['players']
        else:
            self.players = []
        if 'id' in kwargs:
            self.id =  kwargs['id']
        else:
            self.id = False
        if 'round' in kwargs:
            self.round =  kwargs['round']
        else:
            self.round = 0
        if 'registered' in kwargs:
            self.registered =  kwargs['registered']
        else:
            self.registered = False
        if 'started' in kwargs:
            self.started =  kwargs['started']
        else:
            self.started = False
        if 'finished' in kwargs:
            self.finished =  kwargs['finished']
        else:
            self.finished = False


    def __repr__(self) -> str:
        first_part = f"Tournoi n°{self.id}: {self.name} à {self.place} le {self.date}."
        if not self.registered:
            second_part = f"Le tournoi n'est pas enregistré et donc fermé aux inscriptions. Taper (.te) pour l'enregistrer"
        else:
            second_part = f"Il y a {len(self.players)} joueurs inscrits."
        if not self.started:
            third_part = "Le tournoi n'est démarré. Taper (.td) pour le démarrer"
        elif self.finished:
            third_part = f"Le tournoi est terminé"
        else:
            third_part = f"Le tournoi est démarré."
        return first_part + second_part + third_part


    def stringify(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',',': '))


    def serialize(self):
        stringified = self.stringify()
        return json.loads(stringified)


    def register(self, table):
        if not self.id:
            self.id = len(table) + 1
        if not self.registered:
            self.registered = True
            serialized = self.serialize()
            table.insert(Document(serialized, doc_id=self.id))
            return True
        else:
            return False

    def complete_update(self, table):
        if self.registered:
            serialized = self.serialize()
            print(serialized)
            table.update(Document(serialized, doc_id=self.id))

    def add_player(self, id):
        if id not in self.players:
            self.players.append(id)
            return True
        return False

    def new_round(self, round):
        self.round += 1
        self.round_details.append(round)

