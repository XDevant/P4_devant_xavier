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
        self.default_raw_command = None
        self.menu = None
        self.last_command = ""
        self.next_command = None
