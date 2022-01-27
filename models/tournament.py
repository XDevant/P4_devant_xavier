import json

class Tournament:
    def __init__(self, name, place, date, timer, description="", rounds=4):
        self.name = name
        self.place = place
        self.date = date
        self.rounds = rounds
        self.round = 0
        self.round_details =[]
        self.players = []
        self.timer = timer
        self.description = description

    def stringify(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',',': '))

    def serialize(self):
        stringified = self.stringify()
        return json.loads(stringified)

    def register(self, table):
        serialized = self.serialize()
        table.insert(serialized)

    def update(self, table):
        serialized = self.stringify()
        table.update(json.loads(serialized))



