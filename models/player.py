import json
from tinydb.table import Document

class Player:
    def __init__(self, last_name, first_name, date_of_brith, gender, ranking=0, id=0, registered=False):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_brith = date_of_brith
        self.gender = gender
        self.ranking = ranking
        self.id = id
        self.points_in_tournament = 0
        self.registered = registered


    def stringify(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',',': '))

    def serialize(self):
        stringified = self.stringify()
        return json.loads(stringified)

    def register(self, table):
        if self.id == 0:
            self.id = 1 + len(table)
        if self.ranking == 0:
            self.ranking = self.id
        serialized = self.serialize()
        if not self.registered:
            table.insert(Document(serialized, doc_id=self.id))

    def complete_update(self, table):
        serialized = self.stringify()
        table.update(json.loads(serialized))