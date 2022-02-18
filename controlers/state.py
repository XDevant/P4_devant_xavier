class State:
    def __init__(self):
        self.new_player = {}
        self.new_tournament = {}
        self.new_round = {}
        self.update_player = {}
        self.update_tournament = {}
        self.update_round = {}
        self.default_player = None
        self.default_tournament = None
        self.default_command = None
        self.menu = None
        self.last_command = ""
        self.next_command = None
        self.next_key = None


    def __repr__(self):
        keys = [attrib for attrib in dir(self) if not callable(getattr(self, attrib)) and not attrib.startswith('__')]
        return "".join([f"{key}: {getattr(self, key)}\n" for key in keys])
