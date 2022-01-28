from datetime import datetime

class Round:
    def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name =  kwargs['name']
        else:
            self.name = None
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
        self.matches = [match for match in args]