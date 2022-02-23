class Feedback:
    def __init__(self):
        self.title = ""
        self.input = None
        self.raw_command = None
        self.raw_value = None
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

