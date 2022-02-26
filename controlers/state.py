class State:
    def __init__(self, **kwargs):
        self.new_player = {}
        if 'new_player' in kwargs:
            self.new_player = kwargs['new_player']
        self.new_tournament = {}
        if 'new_tournament' in kwargs:
            self.new_tournament = kwargs['new_tournament']
        self.new_round = {}
        if 'new_round' in kwargs:
            self.new_round = kwargs['new_round']
        self.update_player = {}
        if 'update_player' in kwargs:
            self.update_player = kwargs['update_player']
        self.update_tournament = {}
        if 'update_tournament' in kwargs:
            self.update_tournament = kwargs['update_tournament']
        self.update_round = {}
        if 'update_round' in kwargs:
            self.update_round = kwargs['update_tournament']
        self.start_tournament = {}
        if 'start_tournament' in kwargs:
            self.start_tournament = kwargs['start_tournament']
        self.active_tournament = None
        if 'active_tournament' in kwargs:
            self.active_tournament = kwargs['active_tournament']
        self.default_tournament = None
        if 'default_tournament' in kwargs:
            self.default_tournament = kwargs['default_tournament']
        self.default_command = None
        if 'default_command' in kwargs:
            self.default_command = kwargs['default_command']
        self.last_command = ""
        if 'last_command' in kwargs:
            self.last_command = kwargs['last_command']
        self.next_keys = []
        if 'next_keys' in kwargs:
            self.next_keys = kwargs['next_keys']
        self.validation = False
        if 'validation' in kwargs:
            self.validation = kwargs['validation']
        self.prediction = False
        if 'prediction' in kwargs:
            self.prediction = kwargs['prediction']
        self.ignore_default = False
        if 'ignore_default' in kwargs:
            self.ignore_default = kwargs['ignore_default']

    def __repr__(self):
        keys = [a for a in dir(self) if not (callable(getattr(self, a)) or a.startswith('_'))]
        return "".join([f"{key}: {getattr(self, key)}\n" for key in keys])

    def serialize(self):
        keys = [a for a in dir(self) if not (callable(getattr(self, a)) or a.startswith('_'))]
        serialized = {key: getattr(self, key) for key in keys}
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
        dict = {key: value for key, value in feedback.values.items() if value is not None}
        setattr(self, feedback.command, dict)

    def validation_failure(self, feedback):
        self.validation = False
        setattr(self, feedback.command, {})
        self.default_command = feedback.command
        self.next_keys = []
        feedback.success = True

    def validation_started(self, feedback):
        feedback.success = True
        self.validation = True
        self.default_command = feedback.command
        self.next_keys = []

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
            n = self.default_tournament
            feedback.info = f"Le tournoi n°{n} n'est plus le tournoi par défaut."
            self.default_tournament = None

    def start_ok(self, feedback, tournament_id, next_command):
        self.default_command = next_command
        self.next_keys = ["player_id"]
        self.active_tournament = tournament_id
        self.last_command = feedback.command
        self.validation = False
        
    def clear_menu(self):
        self.default_command = None
        self.next_keys = []
