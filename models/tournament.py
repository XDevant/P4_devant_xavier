from datetime import date
from models.round import Round


class Tournament:
    def __init__(self, db, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            self.name = None
        if 'place' in kwargs:
            self.place = kwargs['place']
        else:
            self.place = None
        if 'date' in kwargs:
            self.date = kwargs['date']
        else:
            self.date = str(date.today())
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = 'No Description'
        if 'rounds' in kwargs:
            self.rounds = kwargs['rounds']
        else:
            self.rounds = 4
        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            self.type = 'blitz'
        if 'round_details' in kwargs and len(kwargs['round_details']) > 0:
            table = db.table("rounds")
            round_list = [table.get(doc_id=id) for id in kwargs['round_details']]
            self.round_details = [Round(**round) for round in round_list]
        else:
            self.round_details = []
        if 'players' in kwargs:
            self.players = kwargs['players']
        else:
            self.players = []
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = False
        if 'round' in kwargs:
            self.round = kwargs['round']
        else:
            self.round = 0
        if 'registered' in kwargs:
            self.registered = kwargs['registered']
        else:
            self.registered = False
        if 'started' in kwargs:
            self.started = kwargs['started']
        else:
            self.started = False
        if 'finished' in kwargs:
            self.finished = kwargs['finished']
        else:
            self.finished = False

    def __repr__(self) -> str:
        part_1 = f"Tournoi n°{self.id}: {self.name} à {self.place} le {self.date}."
        if not self.registered:
            part_2 = "Le tournoi n'est pas enregistré et donc fermé aux inscriptions."
            part_2 += "\nTaper (.te) pour l'enregistrer."
        else:
            part_2 = f"Il y a {len(self.players)} joueurs inscrits"
            if len(self.players) > 0:
                part_2 += ": " + str(self.players) + ". "
            else:
                part_2 += '. '
        if not self.started:
            part_3 = "Le tournoi n'est pas démarré. \n"
        elif self.finished:
            part_3 = "Le tournoi est terminé. \n"
        else:
            part_3 = "Le tournoi est démarré. \n"
        if len(self.round_details) > 0:
            part_3 += str(self.round_details)
        return part_1 + part_2 + part_3

    def serialize(self, db):
        keys = [a for a in dir(self) if not (callable(getattr(self, a)) or a.startswith('_'))]
        serialized = {key: getattr(self, key) for key in keys}
        serialized['round_details'] = []
        for round in self.round_details:
            round_id = round.complete_update(db)
            serialized['round_details'].append(round_id)
        return serialized

    def register(self, db):
        table = db.table("tournaments")
        if not self.registered:
            self.registered = True
            serialized = self.serialize(db)
            doc_id = table.insert(serialized)
            self.id = doc_id
            serialized = self.serialize(db)
            table.update(serialized, doc_ids=[self.id])
            return True
        else:
            return False

    def complete_update(self, db):
        table = db.table("tournaments")
        if self.registered:
            serialized = self.serialize(db)
            table.update(serialized, doc_ids=[self.id])
            return self.id
        return -1

    def add_player(self, id):
        if id not in self.players:
            self.players.append(id)
            return id
        return -1

    def remove_player(self, id):
        if id in self.players:
            index = self.players.index(id)
            return self.players.pop(index)
        return -1

    def new_round(self, round):
        self.round += 1
        self.round_details.append(round)
