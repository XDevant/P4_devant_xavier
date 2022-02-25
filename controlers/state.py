class State:
    def __init__(self):
        self.new_player = {}
        self.new_tournament = {}
        self.new_round = {}
        self.update_player = {}
        self.update_tournament = {}
        self.update_round = {}
        self.start_tournament = {}
        self.active_tournament = None
        self.default_tournament = None
        self.default_command = None
        self.last_command = ""
        self.next_keys = []
        self.validation = False
        self.prediction = False
        self.ignore_default = False


    def __repr__(self):
        keys = [attrib for attrib in dir(self) if not callable(getattr(self, attrib)) and not attrib.startswith('__')]
        return "".join([f"{key}: {getattr(self, key)}\n" for key in keys])


    def serialize(self):
        keys = [attrib for attrib in dir(self) if not callable(getattr(self, attrib)) and not attrib.startswith('__')]
        serialized = {key : getattr(self, key) for key in keys}
        return serialized


    def register(self, db):
        table = db.table("save")
        table.truncate()
        serialized = self.serialize()
        table.insert(serialized)
        return True


    def parsing_failure(self, feedback):
        self.default_command = feedback.command
        self.next_keys = feedback.next_keys
        setattr(self, feedback.command, {key: value for key, value in feedback.values.items() if value is not None})


    def validation_failure(self, feedback):
        self.validation = False
        setattr(self, feedback.command, {})
        self.default_command = feedback.command
        self.next_keys = []
        feedback.success = True


    def execute_succes(self, feedback):
        setattr(self, feedback.command, {})
        self.last_command = feedback.command
        self.next_keys = []
        feedback.succes = True


    def execute_refused(self, feedback, check):
        setattr(self, feedback.command, {})
        self.default_command = feedback.command
        self.next_keys = ["player_id"]
        feedback.succes = False
        if check:
            feedback.info = f"Le tournoi {self.default_tournament} n'est plus le tournoi par défaut."
            self.default_tournament = None

    def start_ok(self, feedback, tournament_id, next_command):
        self.default_command = next_command
        self.next_keys = ["player_id"]
        self.active_tournament = tournament_id
        self.last_command = feedback.command
        self.validation = False