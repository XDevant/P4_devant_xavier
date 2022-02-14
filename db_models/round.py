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


    def __repr__(self):
        look = self.name + ": "
        for match in self:
            i = 1
            look += "Match {i}: " + str(match)
            i += 1
        return look


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