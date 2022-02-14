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
        if not self.id:
            self.id = len(table) + 1
        if not self.started:
            self.started = True
            serialized = self.serialize()
            table.insert(Document(serialized, doc_id=self.id))
            return True
        else:
            return False


    def complete_update(self, db):
        if self.started:
            serialized = self.serialize()
            print(serialized)
            db.table("rounds").update(Document(serialized, doc_id=self.id))
        return self.id


    def start(self):
        if self.started:
            return False
        else:
            self.started = datetime.today()
            return True


    def validate(self):
        check = len(self.matches) > 0
        for match in self.matches:
            if match[0][1] is None or match[1][1] is None:
                check = False
                break
        if self.ended or not check:
            return False
        else:
            self.ended = datetime.today()
            return True


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