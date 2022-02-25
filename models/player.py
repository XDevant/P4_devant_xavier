
class Player:
    def __init__(self, **kwargs):
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        else:
            self.last_name = None
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        else:
            self.first_name = None
        if 'date_of_birth' in kwargs:
            self.date_of_birth = kwargs['date_of_birth']
        else:
            self.date_of_birth = None
        if 'gender' in kwargs:
            self.gender = kwargs['gender']
        else:
            self.gender = None
        if 'ranking' in kwargs:
            self.ranking = kwargs['ranking']
        else:
            self.ranking = 'auto'
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = None
        if 'registered' in kwargs:
            self.registered = kwargs['registered']
        else:
            self.registered = False

    def __repr__(self) -> str:
        return f"({self.id}){self.first_name} {self.last_name} classement: {self.ranking}"

    def serialize(self):
        keys = [a for a in dir(self) if not (callable(getattr(self, a)) or a.startswith('_'))]
        serialized = {key: getattr(self, key) for key in keys}
        return serialized

    def register(self, db):
        if not self.registered:
            self.registered = True
            table = db.table("players")
            serialized = self.serialize()
            doc_id = table.insert(serialized)
            self.id = doc_id
            if self.ranking == 'auto':
                self.ranking = self.id
            serialized = self.serialize()
            table.update(serialized, doc_ids=[self.id])
            return True
        else:
            return False

    def complete_update(self, db):
        if self.registered:
            serialized = self.serialize()
            db.table("players").update(serialized, doc_ids=[self.id])
            return self.id
        return -1
