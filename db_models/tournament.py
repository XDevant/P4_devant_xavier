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
        if 'rounds' in kwargs:
            self.rounds =  kwargs['rounds']
        else:
            self.rounds = 4
        if 'round' in kwargs:
            self.round =  kwargs['round']
        else:
            self.round = 0
        if 'timer' in kwargs:
            self.timer =  kwargs['timer']
        else:
            self.timer = 'blitz'
        if 'description' in kwargs:
            self.description =  kwargs['description']
        else:
            self.description = 'No Description'
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
        if 'registered' in kwargs:
            self.registered =  kwargs['registered']
        else:
            self.registered = False

    def stringify(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',',': '))

    def serialize(self):
        stringified = self.stringify()
        return json.loads(stringified)

    def register(self, table):
        if not self.id:
            self.id = 1 + len(table)
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
            table.update(serialized, doc_id=self.id)

    def add_player(self, id):
        self.players.append(id)

