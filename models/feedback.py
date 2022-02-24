class Feedback:
    def __init__(self):
        self.title = ""
        self.input = None
        self.raw_command = None
        self.raw_values = []
        self.raw_values_save = []
        self.command = None
        self.next_command = None
        self.next_keys = []
        self.values = {}
        self.predicted_values = {}
        self.errors = []
        self.data = []
        self.matches = []
        self.important = ""
        self.info = ""
        self.hint = ""
        self.example = ""
        self.parsed = False
        self.success = False


    def prepare_prediction(self, state):
        self.raw_values_save = self.raw_values
        self.raw_values = []
        self.values = {}
        state.prediction = True
        self.next_command = state.default_command


    def post_prediction(self, state):
        self.raw_values = self.raw_values_save
        state.prediction = False
        state.next_keys = self.next_keys