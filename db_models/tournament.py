from tinydb.table import Document
from datetime import date
from db_models.round import Round


class Tournament:
    def __init__(self, db, **kwargs):
        if 'name' in kwargs:
            self.name =  kwargs['name']
        else:
            self.name = None
        if 'place' in kwargs:
            self.place =  kwargs['place']
        else:
            self.place = None
        if 'date' in kwargs:
            self.date =  kwargs['date']
        else:
            self.date = str(date.today())
        if 'description' in kwargs:
            self.description =  kwargs['description']
        else:
            self.description = 'No Description'
        if 'rounds' in kwargs:
            self.rounds =  kwargs['rounds']
        else:
            self.rounds = 4
        if 'type' in kwargs:
            self.type =  kwargs['type']
        else:
            self.type = 'blitz'
        if 'round_details' in kwargs and len(kwargs['round_details']) > 0:
            round_list = [db.table("rounds").get(doc_id=id) for id in kwargs['round_details']]
            self.round_details = [Round(**round) for round in round_list] # need chk
        else:
            self.round_details = []
        if 'players' in kwargs:
            self.players =  kwargs['players']
        else:
            self.players = []
        if 'id' in kwargs:
            self.id =  kwargs['id']
        else:
            self.id = False
        if 'round' in kwargs:
            self.round =  kwargs['round']
        else:
            self.round = 0
        if 'registered' in kwargs:
            self.registered =  kwargs['registered']
        else:
            self.registered = False
        if 'started' in kwargs:
            self.started =  kwargs['started']
        else:
            self.started = False
        if 'finished' in kwargs:
            self.finished =  kwargs['finished']
        else:
            self.finished = False


    def __repr__(self) -> str:
        first_part = f"Tournoi n°{self.id}: {self.name} à {self.place} le {self.date}. "
        if not self.registered:
            second_part = f"Le tournoi n'est pas enregistré et donc fermé aux inscriptions.\n Taper (.te) pour l'enregistrer. "
        else:
            second_part = f"Il y a {len(self.players)} joueurs inscrits"
            if len(self.players) > 0:
                second_part += ": " + str(self.players) + ". "
            else:
                second_part += '. '
        if not self.started:
            third_part = "Le tournoi n'est pas démarré. \n"
        elif self.finished:
            third_part = f"Le tournoi est terminé. \n"
        else:
            third_part = f"Le tournoi est démarré. \n"
        if len(self.round_details) > 0:
            third_part += str(self.round_details)
        return first_part + second_part + third_part


    def serialize(self, db):
        keys = [attrib for attrib in dir(self) if not callable(getattr(self, attrib)) and not attrib.startswith('__')]
        serialized = {key : getattr(self, key) for key in keys}
        print(self.round_details)
        serialized['round_details'] = []
        for round in self.round_details:
            round_id = round.complete_update(db)
            serialized['round_details'].append(round_id)
        print(serialized)
        return serialized


    def register(self, db):
        table = db.table("tournaments")
        if not self.id:
            self.id = len(table) + 1
        if not self.registered:
            self.registered = True
            serialized = self.serialize(db)
            table.insert(Document(serialized, doc_id=self.id))
            return True
        else:
            return False

    def complete_update(self, db):
        if self.registered:
            serialized = self.serialize(db)
            db.table("tournaments").update(Document(serialized, doc_id=self.id))

    def add_player(self, id):
        if id not in self.players:
            self.players.append(id)
            return True
        return False

    def new_round(self, round):
        self.round += 1
        self.round_details.append(round)

