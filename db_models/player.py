import json
from tinydb.table import Document

class Player:
    def __init__(self, **kwargs):
        if 'last_name' in kwargs:
            self.last_name =  kwargs['last_name']
        else:
            self.last_name = None
        if 'first_name' in kwargs:
            self.first_name =  kwargs['first_name']
        else:
            self.first_name = None
        if 'date_of_birth' in kwargs:
            self.date_of_birth =  kwargs['date_of_birth']
        else:
            self.date_of_birth = None
        if 'gender' in kwargs:
            self.gender =  kwargs['gender']
        else:
            self.gender = None
        if 'ranking' in kwargs:
            self.ranking =  kwargs['ranking']
        else:
            self.ranking = 'auto'
        if 'id' in kwargs:
            self.id =  kwargs['id']
        else:
            self.id = None
        if 'registered' in kwargs:
            self.registered =  kwargs['registered']
        else:
            self.registered = False

    
    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name} id: {self.id} classement: {self.ranking}"

    def stringify(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',',': '))

    def serialize(self):
        stringified = self.stringify()
        return json.loads(stringified)

    def register(self, table):
        if not self.id:
            self.id = 1 + len(table)
        if self.ranking == 'auto':
            self.ranking = self.id
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