from datetime import datetime
from tinydb.table import Document


class Round:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name =  kwargs['name']
        else:
            self.name = "Round "
        if 'tournament' in kwargs:
            self.tournament = kwargs['tournament']
        else:
            self.tournament = None
        if 'matches' in kwargs:
            self.matches =  kwargs['matches']
        else:
            self.matches = []
        if 'started' in kwargs:
            self.started =  kwargs['started']
        else:
            self.started = False
        if 'ended' in kwargs:
            self.ended =  kwargs['ended']
        else:
            self.ended = False
        if 'id' in kwargs:
            self.id =  kwargs['id']
        else:
            self.id = False


    def __iter__(self):
        return self.matches.__iter__()


    def __repr__(self):
        look = self.name + ": "
        i = 1
        for match in self:
            look += f", Match {i}: " + str(match)
            i += 1
        return look


    def serialize(self):
        keys = [attrib for attrib in dir(self) if not callable(getattr(self, attrib)) and not attrib.startswith('__')]
        serialized = {key : getattr(self, key) for key in keys}
        return serialized


    def register(self, table):
        if not self.started:
            self.start()
            serialized = self.serialize()
            doc_id = table.insert(serialized)
            self.id = doc_id
            serialized = self.serialize()
            table.update(serialized, doc_ids=[self.id])
            return True
        else:
            return False
        


    def complete_update(self, db):
        if self.started:
            serialized = self.serialize()
            return db.table("rounds").update(serialized, doc_ids=[self.id])
        return None


    def start(self):
        if self.started:
            return False
        else:
            self.started = str(datetime.today())
            return True


    def validate(self):
        if self.ended or not len(self.matches) == 0 or self.chech_matches() >= 0:
            return False
        else:
            self.ended = str(datetime.today())
            return True


    def chech_matches(self):
        for i in range(len(self.matches)):
            match = self.matches[i]
            if match[0][1] is None or match[1][1] is None:
                return i
        return -1


    def add_matches(self, *args):
        self.matches = [([match_ids[0], None], [match_ids[1], None]) for match_ids in args]


    def update_match(self, index, points_a, points_b):
        if index < len(self.matches):
            self.matches[index] = ([self.matches[index][0][0], points_a], [self.matches[index][1][0], points_b])
            return True
        else:
            return False


    def find_indexes(self, player_id):
        for i in range(len(self.matches)):
            if self.matches[i][0][0] == player_id:
                return i, 0
            if self.matches[i][1][0] == player_id:
                return i, 1
        return -1, -1