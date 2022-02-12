from datetime import datetime

class Round:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name =  kwargs['name']
        else:
            self.name = "Round "
        if 'matches' in kwargs:
            self.matches =  kwargs['matches']
        else:
            self.matches = []
        if 'started' in kwargs:
            self.started =  kwargs['started']
        else:
            self.started = None
        if 'ended' in kwargs:
            self.ended =  kwargs['ended']
        else:
            self.ended = None


    def __iter__(self):
        return self.matches.__iter__()


    def __str__(self):
        look = self.name + ": "
        for match in self:
            look += str(match)
        return look

    def start(self):
        if self.started:
            return False
        else:
            self.started = datetime.today()
            return True

    def validate(self):
        if self.ended:
            return False
        else:
            self.ended = datetime.today()
            return True

    def add_matches(self, *args):
        self.matches = [([match_ids[0], None], [match_ids[1], None]) for match_ids in args]
